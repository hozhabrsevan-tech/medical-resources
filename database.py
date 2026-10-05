import sqlite3


DB_NAME = "database.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            file_id TEXT,
            link TEXT,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_resource(
    title,
    category,
    resource_type,
    file_id=None,
    link=None,
    description=None
):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resources
        (
            title,
            category,
            resource_type,
            file_id,
            link,
            description
        )

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        category,
        resource_type,
        file_id,
        link,
        description
    ))

    conn.commit()
    conn.close()


def show_resources(category):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, resource_type
        FROM resources
        WHERE category = ?
    """, (category,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_resource(resource_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            category,
            resource_type,
            file_id,
            link,
            description
        FROM resources
        WHERE id = ?
    """, (resource_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def search_resources(keyword):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, category
        FROM resources
        WHERE title LIKE ?
    """, (f"%{keyword}%",))

    rows = cursor.fetchall()

    conn.close()

    return rows


def add_favorite(user_id, resource_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO favorites
        (
            user_id,
            resource_id
        )
        VALUES (?, ?)
    """, (
        user_id,
        resource_id
    ))

    conn.commit()
    conn.close()