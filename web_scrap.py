import database
import backend
import html
import webbrowser
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

HTML_FILE = "studios.html"


# ============================================================
# HTML GENERATION
# ============================================================

def generate_html(studios):
    """
    Generate a clean, searchable and filterable HTML dashboard
    containing all scraped game studios.
    """

    # --------------------------------------------------------
    # Prepare studio rows
    # --------------------------------------------------------

    rows = []

    for studio in studios:

        name = studio[1] or ""
        city = studio[2] or ""
        state = studio[3] or ""
        studio_type = studio[4] or ""
        website = studio[5] or ""
        source = studio[7] or ""

        # Escape text so HTML remains safe
        safe_name = html.escape(name)
        safe_city = html.escape(city)
        safe_state = html.escape(state)
        safe_type = html.escape(studio_type)
        safe_source = html.escape(source)

        # Website
        if website:

            safe_website = html.escape(website, quote=True)

            website_html = (
                f'<a class="website-link" '
                f'href="{safe_website}" '
                f'target="_blank" '
                f'rel="noopener noreferrer">'
                f'Visit Website ↗'
                f'</a>'
            )

        else:

            website_html = '<span class="no-website">Not available</span>'

        rows.append(
            f"""
            <tr>
                <td class="studio-name">{safe_name}</td>
                <td>{safe_city}</td>
                <td>{safe_state}</td>
                <td>
                    <span class="type-badge">
                        {safe_type}
                    </span>
                </td>
                <td>{website_html}</td>
                <td>{safe_source}</td>
            </tr>
            """
        )

    rows_html = "\n".join(rows)

    # --------------------------------------------------------
    # Generate complete HTML document
    # --------------------------------------------------------

    html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>India Game Studio Directory</title>


<style>

/* =========================================================
   GLOBAL
   ========================================================= */

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Arial,
        sans-serif;

    background: #f4f6f8;

    color: #1f2937;
}}


/* =========================================================
   HEADER
   ========================================================= */

.header {{

    background:
        linear-gradient(
            135deg,
            #111827,
            #1f2937
        );

    color: white;

    padding: 35px 25px;

    text-align: center;

    box-shadow:
        0 4px 15px rgba(0, 0, 0, 0.15);
}}

.header h1 {{

    margin: 0 0 8px;

    font-size: 32px;
}}

.header p {{

    margin: 0;

    color: #d1d5db;

    font-size: 15px;
}}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.container {{

    max-width: 1400px;

    margin: 30px auto;

    padding: 0 20px;
}}


/* =========================================================
   STAT CARD
   ========================================================= */

.stats {{

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));

    gap: 18px;

    margin-bottom: 25px;
}}

.stat-card {{

    background: white;

    padding: 22px;

    border-radius: 12px;

    box-shadow:
        0 2px 10px rgba(0, 0, 0, 0.08);

    border: 1px solid #e5e7eb;
}}

.stat-card .number {{

    font-size: 32px;

    font-weight: 700;

    margin-bottom: 5px;
}}

.stat-card .label {{

    color: #6b7280;

    font-size: 14px;
}}


/* =========================================================
   FILTER PANEL
   ========================================================= */

.filters {{

    background: white;

    padding: 22px;

    border-radius: 12px;

    box-shadow:
        0 2px 10px rgba(0, 0, 0, 0.08);

    margin-bottom: 25px;

    border: 1px solid #e5e7eb;
}}

.filters-title {{

    font-size: 18px;

    font-weight: 600;

    margin-bottom: 15px;
}}

.filter-grid {{

    display: grid;

    grid-template-columns:
        2fr 1fr 1fr;

    gap: 12px;
}}

.filter-input,
.filter-select {{

    width: 100%;

    padding: 12px 14px;

    border: 1px solid #d1d5db;

    border-radius: 8px;

    font-size: 14px;

    background: white;

    outline: none;
}}

.filter-input:focus,
.filter-select:focus {{

    border-color: #6b7280;

    box-shadow:
        0 0 0 3px rgba(107, 114, 128, 0.12);
}}


/* =========================================================
   RESULTS INFO
   ========================================================= */

.results-info {{

    margin: 15px 0;

    color: #6b7280;

    font-size: 14px;
}}


/* =========================================================
   TABLE CONTAINER
   ========================================================= */

.table-container {{

    background: white;

    border-radius: 12px;

    overflow-x: auto;

    box-shadow:
        0 2px 10px rgba(0, 0, 0, 0.08);

    border: 1px solid #e5e7eb;
}}


/* =========================================================
   TABLE
   ========================================================= */

table {{

    width: 100%;

    border-collapse: collapse;

    min-width: 850px;
}}

thead {{

    background: #111827;

    color: white;
}}

th {{

    padding: 15px 14px;

    text-align: left;

    font-size: 13px;

    font-weight: 600;

    cursor: pointer;

    white-space: nowrap;

    user-select: none;
}}

th:hover {{

    background: #374151;
}}

td {{

    padding: 14px;

    border-bottom: 1px solid #e5e7eb;

    font-size: 14px;

    vertical-align: middle;
}}

tbody tr:hover {{

    background: #f9fafb;
}}

.studio-name {{

    font-weight: 600;

    color: #111827;
}}


/* =========================================================
   TYPE BADGE
   ========================================================= */

.type-badge {{

    display: inline-block;

    padding: 5px 9px;

    background: #eef2ff;

    color: #3730a3;

    border-radius: 20px;

    font-size: 12px;

    font-weight: 600;

    white-space: nowrap;
}}


/* =========================================================
   WEBSITE
   ========================================================= */

.website-link {{

    display: inline-block;

    padding: 7px 11px;

    background: #111827;

    color: white;

    text-decoration: none;

    border-radius: 6px;

    font-size: 12px;

    font-weight: 600;

    transition: 0.2s;
}}

.website-link:hover {{

    background: #374151;

    transform: translateY(-1px);
}}

.no-website {{

    color: #9ca3af;

    font-size: 12px;
}}


/* =========================================================
   NO RESULTS
   ========================================================= */

.no-results {{

    text-align: center;

    padding: 50px;

    color: #6b7280;

    display: none;
}}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {{

    text-align: center;

    padding: 30px 20px;

    color: #6b7280;

    font-size: 13px;
}}

.footer strong {{

    color: #374151;
}}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 800px) {{

    .filter-grid {{

        grid-template-columns: 1fr;
    }}

    .header h1 {{

        font-size: 25px;
    }}

    .container {{

        padding: 0 12px;
    }}
}}

</style>

</head>


<body>


<!-- =======================================================
     HEADER
     ======================================================= -->

<div class="header">

    <h1>🎮 India Game Studio Directory</h1>

    <p>
        Game studios, developers, publishers and gaming companies
        across India
    </p>

</div>


<!-- =======================================================
     MAIN
     ======================================================= -->

<div class="container">


    <!-- ===================================================
         STATISTICS
         =================================================== -->

    <div class="stats">

        <div class="stat-card">

            <div
                class="number"
                id="totalStudios">
                {len(studios)}
            </div>

            <div class="label">
                Total Studios
            </div>

        </div>


        <div class="stat-card">

            <div
                class="number"
                id="visibleStudios">
                {len(studios)}
            </div>

            <div class="label">
                Matching Results
            </div>

        </div>


        <div class="stat-card">

            <div
                class="number"
                id="stateCount">
                -
            </div>

            <div class="label">
                States / Regions
            </div>

        </div>


        <div class="stat-card">

            <div
                class="number"
                id="typeCount">
                -
            </div>

            <div class="label">
                Studio Types
            </div>

        </div>

    </div>


    <!-- ===================================================
         FILTERS
         =================================================== -->

    <div class="filters">

        <div class="filters-title">
            🔎 Search & Filter
        </div>


        <div class="filter-grid">


            <!-- SEARCH -->

            <input
                type="text"
                id="searchInput"
                class="filter-input"
                placeholder="Search by studio name..."
                onkeyup="filterTable()"
            >


            <!-- STATE -->

            <select
                id="stateFilter"
                class="filter-select"
                onchange="filterTable()"
            >

                <option value="">
                    📍 All States
                </option>

            </select>


            <!-- TYPE -->

            <select
                id="typeFilter"
                class="filter-select"
                onchange="filterTable()"
            >

                <option value="">
                    🎮 All Studio Types
                </option>

            </select>


        </div>

    </div>


    <!-- ===================================================
         RESULTS INFO
         =================================================== -->

    <div class="results-info">

        Showing
        <strong id="resultText">
            {len(studios)}
        </strong>
        studios

    </div>


    <!-- ===================================================
         TABLE
         =================================================== -->

    <div class="table-container">

        <table id="studioTable">

            <thead>

                <tr>

                    <th onclick="sortTable(0)">
                        Studio Name ↕
                    </th>

                    <th onclick="sortTable(1)">
                        City ↕
                    </th>

                    <th onclick="sortTable(2)">
                        State ↕
                    </th>

                    <th onclick="sortTable(3)">
                        Studio Type ↕
                    </th>

                    <th>
                        Website
                    </th>

                    <th onclick="sortTable(5)">
                        Source ↕
                    </th>

                </tr>

            </thead>


            <tbody>

                {rows_html}

            </tbody>

        </table>


        <div
            id="noResults"
            class="no-results">

            <h3>No studios found</h3>

            <p>
                Try changing your search or filter.
            </p>

        </div>

    </div>


</div>


<!-- =======================================================
     FOOTER
     ======================================================= -->

<div class="footer">

    Data source:
    <strong>GameDevMap</strong>

    <br><br>

    Generated automatically by the
    <strong>India Game Studio Scraper</strong>

</div>


<!-- =======================================================
     JAVASCRIPT
     ======================================================= -->

<script>


// ==========================================================
// INITIAL DATA
// ==========================================================

const table =
    document.getElementById("studioTable");

const tbody =
    table.querySelector("tbody");

const rows =
    Array.from(tbody.querySelectorAll("tr"));


// ==========================================================
// CREATE FILTER OPTIONS
// ==========================================================

function createFilters() {{

    const stateFilter =
        document.getElementById("stateFilter");

    const typeFilter =
        document.getElementById("typeFilter");


    const states = new Set();

    const types = new Set();


    rows.forEach(row => {{

        const cells = row.children;


        const state =
            cells[2].textContent.trim();

        const type =
            cells[3].textContent.trim();


        if (state) {{
            states.add(state);
        }}

        if (type) {{
            types.add(type);
        }}

    }});


    // ------------------------------------------------------
    // States
    // ------------------------------------------------------

    Array.from(states)
        .sort()
        .forEach(state => {{

            const option =
                document.createElement("option");

            option.value = state;

            option.textContent = state;

            stateFilter.appendChild(option);

        }});


    // ------------------------------------------------------
    // Types
    // ------------------------------------------------------

    Array.from(types)
        .sort()
        .forEach(type => {{

            const option =
                document.createElement("option");

            option.value = type;

            option.textContent = type;

            typeFilter.appendChild(option);

        }});


    // Update statistics

    document.getElementById("stateCount")
        .textContent = states.size;

    document.getElementById("typeCount")
        .textContent = types.size;

}}


// ==========================================================
// SEARCH + FILTER
// ==========================================================

function filterTable() {{

    const search =
        document
            .getElementById("searchInput")
            .value
            .toLowerCase()
            .trim();


    const selectedState =
        document
            .getElementById("stateFilter")
            .value
            .toLowerCase();


    const selectedType =
        document
            .getElementById("typeFilter")
            .value
            .toLowerCase();


    let visibleCount = 0;


    rows.forEach(row => {{

        const cells = row.children;


        const name =
            cells[0]
                .textContent
                .toLowerCase();


        const state =
            cells[2]
                .textContent
                .toLowerCase();


        const type =
            cells[3]
                .textContent
                .toLowerCase();


        const matchesSearch =
            name.includes(search);


        const matchesState =
            !selectedState ||
            state === selectedState;


        const matchesType =
            !selectedType ||
            type === selectedType;


        const visible =
            matchesSearch &&
            matchesState &&
            matchesType;


        row.style.display =
            visible ? "" : "none";


        if (visible) {{
            visibleCount++;
        }}

    }});


    // ------------------------------------------------------
    // Update result count
    // ------------------------------------------------------

    document.getElementById("visibleStudios")
        .textContent = visibleCount;


    document.getElementById("resultText")
        .textContent = visibleCount;


    // ------------------------------------------------------
    // No results message
    // ------------------------------------------------------

    const noResults =
        document.getElementById("noResults");


    noResults.style.display =
        visibleCount === 0
            ? "block"
            : "none";


    table.style.display =
        visibleCount === 0
            ? "none"
            : "table";

}}


// ==========================================================
// SORT TABLE
// ==========================================================

function sortTable(columnIndex) {{

    const rowsArray =
        Array.from(tbody.querySelectorAll("tr"));


    const currentDirection =
        table
            .getAttribute(
                "data-sort-direction"
            );


    const currentColumn =
        table
            .getAttribute(
                "data-sort-column"
            );


    let ascending = true;


    if (
        currentColumn == columnIndex &&
        currentDirection === "asc"
    ) {{

        ascending = false;

    }}


    rowsArray.sort((a, b) => {{

        const aText =
            a.children[columnIndex]
                .textContent
                .trim()
                .toLowerCase();


        const bText =
            b.children[columnIndex]
                .textContent
                .trim()
                .toLowerCase();


        if (aText < bText) {{
            return ascending ? -1 : 1;
        }}


        if (aText > bText) {{
            return ascending ? 1 : -1;
        }}


        return 0;

    }});


    rowsArray.forEach(row => {{
        tbody.appendChild(row);
    }});


    table.setAttribute(
        "data-sort-direction",
        ascending ? "asc" : "desc"
    );


    table.setAttribute(
        "data-sort-column",
        columnIndex
    );

}}


// ==========================================================
// START
// ==========================================================

createFilters();

filterTable();

</script>


</body>

</html>
"""

    # --------------------------------------------------------
    # Save HTML file
    # --------------------------------------------------------

    output_path = Path(HTML_FILE)

    output_path.write_text(
        html_content,
        encoding="utf-8"
    )

    return output_path


# ============================================================
# DISPLAY TERMINAL SUMMARY
# ============================================================

def display_summary(studios):
    """Display a short terminal summary."""

    print("\n" + "=" * 70)
    print("DATABASE SUMMARY")
    print("=" * 70)

    print(f"Total studios: {len(studios)}")

    states = set()
    types = set()

    for studio in studios:

        if studio[3]:
            states.add(studio[3])

        if studio[4]:
            types.add(studio[4])

    print(f"States / regions: {len(states)}")
    print(f"Studio types: {len(types)}")

    print("\nFirst 10 studios:")

    print("-" * 70)

    for studio in studios[:10]:

        print(f"Name: {studio[1]}")
        print(f"City: {studio[2] or 'N/A'}")
        print(f"State: {studio[3] or 'N/A'}")
        print(f"Type: {studio[4] or 'N/A'}")
        print(f"Website: {studio[5] or 'N/A'}")
        print("-" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("       INDIA GAME STUDIO DATABASE")
    print("=" * 70)


    # --------------------------------------------------------
    # STEP 1: Initialize database
    # --------------------------------------------------------

    print("\n[1/5] Initializing database...")

    database.initialize_database()


    # --------------------------------------------------------
    # STEP 2: Scrape studios
    # --------------------------------------------------------

    print("\n[2/5] Starting web scraper...")

    scraped_studios = backend.scrape_studios()


    if not scraped_studios:

        print("\nNo studios were scraped.")

        return


    print(
        f"\nSuccessfully scraped "
        f"{len(scraped_studios)} unique studios."
    )


    # --------------------------------------------------------
    # STEP 3: Save to database
    # --------------------------------------------------------

    print("\n[3/5] Saving studios to database...")

    database.add_studios(scraped_studios)


    # --------------------------------------------------------
    # STEP 4: Read database
    # --------------------------------------------------------

    print("\n[4/5] Reading database...")

    all_studios = database.get_all_studios()

    total = database.get_studio_count()

    print(
        f"Total studios currently in database: {total}"
    )


    # --------------------------------------------------------
    # STEP 5: Generate HTML dashboard
    # --------------------------------------------------------

    print("\n[5/5] Generating Chrome dashboard...")

    html_path = generate_html(all_studios)

    print(
        f"\nDashboard created successfully:"
    )

    print(
        f"{html_path.resolve()}"
    )


    # --------------------------------------------------------
    # Terminal summary
    # --------------------------------------------------------

    display_summary(all_studios)


    # --------------------------------------------------------
    # Open dashboard in default browser
    # --------------------------------------------------------

    print("\nOpening dashboard in your browser...")

    webbrowser.open(
        html_path.resolve().as_uri()
    )


    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nFiles:")
    print("  backend.py       → Scrapes GameDevMap")
    print("  database.py      → Handles SQLite database")
    print("  game_studios.db  → Stores studio data")
    print("  studios.html     → Browser dashboard")

    print("\nThe dashboard should now be open in Chrome.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()