# myproject/backend/app/main.py
from fastapi import FastAPI
from app.omdb_service import fetch_movie_by_title
from app.database import get_db_connection, create_table_if_not_exists

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/movies/{title}")
def get_movie(title: str):
    """Fetch movie details from the OMDb API."""
    movie_data = fetch_movie_by_title(title)
    return movie_data

@app.get("/create_table")
def create_table():
    """
    Endpoint to create a simple table for demonstration.
    """
    try:
        create_table_if_not_exists()
        return {"status": "demo_table created (or already exists)."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/insert/{name}")
def insert_name(name: str):
    """
    Insert a 'name' into demo_table for a quick test.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO demo_table (name) VALUES (%s);", (name,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": f"Inserted {name} into demo_table."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/fetch_names")
def fetch_names():
    """
    Fetch and return all names in demo_table.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM demo_table;")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return {"rows": [{"id": row[0], "name": row[1]} for row in rows]}
    except Exception as e:
        return {"error": str(e)}


