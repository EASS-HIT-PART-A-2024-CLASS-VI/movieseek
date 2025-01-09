import os
import mysql.connector

# Read environment variables for DB config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")


def get_db_connection():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def create_table_if_not_exists():
    """
    Create a simple table for demonstration (if it doesn't already exist).
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demo_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
