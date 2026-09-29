import sqlite3
from datetime import datetime


DATABASE_NAME = "game_studios.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """
    Create the studios table if it does not already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS studios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            city TEXT,
            state TEXT,
            studio_type TEXT,
            website TEXT,
            games TEXT,
            source TEXT,
            last_updated TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")


def add_studio(
    name,
    city=None,
    state=None,
    studio_type=None,
    website=None,
    games=None,
    source=None
):
    """
    Add a single game studio to the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO studios (
                name,
                city,
                state,
                studio_type,
                website,
                games,
                source,
                last_updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            city,
            state,
            studio_type,
            website,
            games,
            source,
            last_updated
        ))

        connection.commit()

    except sqlite3.IntegrityError:
        print(f"Studio already exists: {name}")

    finally:
        connection.close()


def add_studios(studios):
    """
    Add multiple studios to the database.

    studios should be a list of dictionaries.
    """

    connection = get_connection()
    cursor = connection.cursor()

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for studio in studios:

        try:
            cursor.execute("""
                INSERT INTO studios (
                    name,
                    city,
                    state,
                    studio_type,
                    website,
                    games,
                    source,
                    last_updated
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                studio.get("name"),
                studio.get("city"),
                studio.get("state"),
                studio.get("studio_type"),
                studio.get("website"),
                studio.get("games"),
                studio.get("source"),
                last_updated
            ))

        except sqlite3.IntegrityError:
            print(
                f"Skipping duplicate studio: "
                f"{studio.get('name')}"
            )

    connection.commit()
    connection.close()

    print(f"{len(studios)} studio records processed.")


def get_all_studios():
    """
    Return all studios from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            city,
            state,
            studio_type,
            website,
            games,
            source,
            last_updated
        FROM studios
        ORDER BY name
    """)

    studios = cursor.fetchall()

    connection.close()

    return studios


def search_studios(keyword):
    """
    Search studios by name, city, state, type, or games.
    """

    connection = get_connection()
    cursor = connection.cursor()

    search_term = f"%{keyword}%"

    cursor.execute("""
        SELECT
            id,
            name,
            city,
            state,
            studio_type,
            website,
            games,
            source,
            last_updated
        FROM studios
        WHERE
            name LIKE ?
            OR city LIKE ?
            OR state LIKE ?
            OR studio_type LIKE ?
            OR games LIKE ?
        ORDER BY name
    """, (
        search_term,
        search_term,
        search_term,
        search_term,
        search_term
    ))

    results = cursor.fetchall()

    connection.close()

    return results


def get_studios_by_state(state):
    """
    Return all studios from a particular state.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            city,
            state,
            studio_type,
            website,
            games,
            source,
            last_updated
        FROM studios
        WHERE state LIKE ?
        ORDER BY name
    """, (f"%{state}%",))

    studios = cursor.fetchall()

    connection.close()

    return studios


def delete_studio(studio_id):
    """
    Delete a studio using its database ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM studios
        WHERE id = ?
    """, (studio_id,))

    connection.commit()
    connection.close()

    print(f"Studio with ID {studio_id} deleted.")


def get_studio_count():
    """
    Return the total number of studios in the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM studios
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


if __name__ == "__main__":
    initialize_database()