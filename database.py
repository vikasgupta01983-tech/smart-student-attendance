import sqlite3


def create_database():
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()

    # Create students table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            password_hash TEXT
        )
    """)

    # Add password_hash to an existing database if needed
    cursor.execute("PRAGMA table_info(students)")
    columns = [column[1] for column in cursor.fetchall()]

    if "password_hash" not in columns:
        cursor.execute("""
            ALTER TABLE students
            ADD COLUMN password_hash TEXT
        """)

    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_name TEXT NOT NULL,
            session_date TEXT NOT NULL
        )
    """)

    # Create attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            attendance_time TEXT NOT NULL,
            UNIQUE(student_id, session_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database updated successfully!")

