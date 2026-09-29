import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://www.gamedevmap.com/"
INDIA_URL = (
    "https://www.gamedevmap.com/index.php"
    "?city=&country=India&query=&state=&type=&count=100"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}

REQUEST_DELAY = 1


# ============================================================
# FETCH PAGE
# ============================================================

def fetch_page(url):
    """Download a webpage and return BeautifulSoup."""

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as error:
        print(f"Error fetching page:")
        print(error)
        return None


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):
    """Clean whitespace from text."""

    if not value:
        return ""

    return " ".join(value.split()).strip()


def clean_studio_name(name):
    """Clean studio/company name."""

    name = clean_text(name)

    return name


# ============================================================
# WEBSITE EXTRACTION
# ============================================================

def extract_website(row):
    """Extract the studio website from a table row."""

    links = row.find_all("a", href=True)

    for link in links:

        href = link.get("href", "").strip()

        if not href:
            continue

        # Ignore GameDevMap internal links
        if "gamedevmap.com" in href.lower():
            continue

        # Convert relative URLs into absolute URLs
        return urljoin(BASE_URL, href)

    return None


# ============================================================
# VALIDATE STUDIO
# ============================================================

def is_valid_studio(studio):
    """Check whether a scraped record is a valid studio."""

    name = studio.get("name", "").strip()

    if not name:
        return False

    # Ignore obvious footer / navigation text
    invalid_phrases = [
        "gamedevmap served",
        "financial support makes it possible",
        "your financial support",
        "copyright",
        "privacy policy",
        "terms of service"
    ]

    name_lower = name.lower()

    for phrase in invalid_phrases:
        if phrase in name_lower:
            return False

    return True


# ============================================================
# SCRAPE ONE PAGE
# ============================================================

def scrape_page(url):
    """
    Scrape one GameDevMap page.

    GameDevMap table structure:

    Company
    Social / extra column
    Type
    City
    State / Province
    Country / Region
    """

    soup = fetch_page(url)

    if soup is None:
        return []

    studios = []

    tables = soup.find_all("table")

    if not tables:
        print("No tables found on page.")
        return []

    for table in tables:

        rows = table.find_all("tr")

        for row in rows:

            cells = row.find_all(["td", "th"])

            if len(cells) < 6:
                continue

            values = [
                clean_text(cell.get_text(" ", strip=True))
                for cell in cells
            ]

            # ------------------------------------------------
            # GameDevMap verified column structure
            # ------------------------------------------------

            name = clean_studio_name(values[0])
            studio_type = clean_text(values[2])
            city = clean_text(values[3])
            state = clean_text(values[4])
            country = clean_text(values[5])

            # We only want India
            if country.lower() != "india":
                continue

            website = extract_website(row)

            studio = {
                "name": name,
                "city": city,
                "state": state,
                "studio_type": studio_type,
                "website": website,
                "games": None,
                "source": "GameDevMap"
            }

            if is_valid_studio(studio):
                studios.append(studio)

    return studios


# ============================================================
# PAGINATION
# ============================================================

def build_page_url(start):
    """
    Build GameDevMap pagination URL.

    First page:
        start = 1

    Second page:
        start = 101

    Third page:
        start = 201

    Each page contains up to 100 records.
    """

    return (
        "https://www.gamedevmap.com/index.php"
        f"?city=&country=India&query=&state=&type="
        f"&count=100&start={start}"
    )


def scrape_all_pages():
    """Scrape all available India pages."""

    all_studios = []

    start = 1
    page_number = 1

    while True:

        url = build_page_url(start)

        print(f"\nPage {page_number}:")
        print(f"Start position: {start}")
        print(f"URL: {url}")

        studios = scrape_page(url)

        print(f"Studios found on this page: {len(studios)}")

        if not studios:
            print("No more studios found.")
            break

        all_studios.extend(studios)

        # ----------------------------------------------------
        # If fewer than 100 records are returned,
        # this is the final page.
        # ----------------------------------------------------

        if len(studios) < 100:
            print("Final page reached.")
            break

        start += 100
        page_number += 1

        time.sleep(REQUEST_DELAY)

    return all_studios


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(studios):
    """
    Remove duplicate records.

    A studio is considered the same if:
        name + city + state
    are identical.
    """

    unique_studios = []
    seen = set()

    for studio in studios:

        name = clean_text(studio.get("name", "")).lower()
        city = clean_text(studio.get("city", "")).lower()
        state = clean_text(studio.get("state", "")).lower()

        key = (name, city, state)

        if key in seen:
            continue

        seen.add(key)
        unique_studios.append(studio)

    return unique_studios


# ============================================================
# CLEAN STUDIO DATA
# ============================================================

def clean_studio_data(studios):
    """Clean and validate all studio records."""

    cleaned = []

    for studio in studios:

        name = clean_studio_name(
            studio.get("name", "")
        )

        city = clean_text(
            studio.get("city", "")
        )

        state = clean_text(
            studio.get("state", "")
        )

        studio_type = clean_text(
            studio.get("studio_type", "")
        )

        website = studio.get("website")

        if website:
            website = website.strip()

        cleaned_studio = {
            "name": name,
            "city": city,
            "state": state,
            "studio_type": studio_type,
            "website": website,
            "games": studio.get("games"),
            "source": "GameDevMap"
        }

        if is_valid_studio(cleaned_studio):
            cleaned.append(cleaned_studio)

    return cleaned


# ============================================================
# MAIN SCRAPER FUNCTION
# ============================================================

def scrape_studios():
    """Main function used by main.py."""

    print("\n" + "=" * 60)
    print("STARTING INDIA GAME STUDIO SCRAPER")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1: Scrape all pages
    # --------------------------------------------------------

    studios = scrape_all_pages()

    print(f"\nRaw studios found: {len(studios)}")

    # --------------------------------------------------------
    # STEP 2: Clean
    # --------------------------------------------------------

    studios = clean_studio_data(studios)

    print(f"After cleaning: {len(studios)}")

    # --------------------------------------------------------
    # STEP 3: Remove duplicates
    # --------------------------------------------------------

    studios = remove_duplicates(studios)

    print(f"After removing duplicates: {len(studios)}")

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)

    return studios


# ============================================================
# TEST BACKEND DIRECTLY
# ============================================================

if __name__ == "__main__":

    studios = scrape_studios()

    print("\n" + "=" * 60)
    print("FIRST 10 STUDIOS")
    print("=" * 60)

    for studio in studios[:10]:

        print(f"\nName: {studio['name']}")
        print(f"City: {studio['city']}")
        print(f"State: {studio['state']}")
        print(f"Type: {studio['studio_type']}")
        print(f"Website: {studio['website']}")
        print(f"Source: {studio['source']}")
        print("-" * 40)

    print(f"\nTOTAL UNIQUE STUDIOS: {len(studios)}")