import sqlite3
DATABASE_NAME = "library.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS libraries(
                library_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, 
                city TEXT, 
                state TEXT, 
                postal_code TEXT
            )
        """,
        """CREATE TABLE IF NOT EXISTS books(
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author_name TEXT, 
                isbn_num TEXT, 
                genre TEXT, 
                description TEXT
            )
        """,
        """CREATE TABLE IF NOT EXISTS library_books(
                library_book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                library_id INTEGER,
                book_id INTEGER, 
                last_library_activity_id INTEGER
            )
        """,
        """CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """,
        """CREATE TABLE IF NOT EXISTS library_activities(
                library_activity_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                activity_type TEXT, user_id INTEGER, 
                user_id INTEGER,
                library_book_id INTEGER, 
                checked_out_at DATETIME, 
                checked_in_at DATETIME
            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
