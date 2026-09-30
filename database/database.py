import sqlite3

# Database file
DATABASE = "phishguard.db"


# Create a connection to the database
def get_connection():
    return sqlite3.connect(DATABASE)


# Create the scans table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            score INTEGER,
            prediction TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Save a scan result
def save_scan(url, score, prediction, explanation=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans
        (url, score, prediction, explanation)
        VALUES (?, ?, ?, ?)
    """, (url, score, prediction, explanation))

    scan_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return scan_id


# Get all saved scans
def get_all_scans():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, url, score, prediction, explanation, created_at
        FROM scans
        ORDER BY id DESC
    """)

    scans = cursor.fetchall()

    conn.close()

    return scans


# Get one specific scan by ID
def get_scan(scan_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, url, score, prediction, explanation, created_at
        FROM scans
        WHERE id = ?
    """, (scan_id,))

    scan = cursor.fetchone()

    conn.close()

    return scan