from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This is a "Model" - it tells FastAPI what a Contact Message looks like
class ContactMessage(BaseModel):
    name: str
    message: str

@app.get("/")
def read_root():
    return {"status": "Portfolio API is running!"}

@app.post("/contact")
def receive_message(data: ContactMessage):
    # For now, we just print it. Soon, this will go to SQL!
    print(f"New message from {data.name}: {data.message}")
    return {"message": "Success! I received your note."}
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # Add this

app = FastAPI()

# Add this block to allow your local HTML file to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd be more specific
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactMessage(BaseModel):
    name: str
    message: str

@app.get("/")
def read_root():
    return {"status": "Portfolio API is running!"}

@app.post("/contact")
def receive_message(data: ContactMessage):
    print(f"New message from {data.name}: {data.message}")
    return {"message": "Success! I received your note."}
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3 # 1. Import the SQL library

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Database Setup: Create a table if it doesn't exist
import os

# Get the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "portfolio.db")

def init_db():
    conn = sqlite3.connect(db_path) # Use the full path
    # ... rest of your code ...
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class ContactMessage(BaseModel):
    name: str
    message: str

@app.get("/")
def read_root():
    return {"status": "Database is ready!"}

@app.post("/contact")
def receive_message(data: ContactMessage):
    # 3. Save the message into the SQL database
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, content) VALUES (?, ?)", (data.name, data.message))
    conn.commit()
    conn.close()
    
    print(f"Saved to SQL: {data.name}")
    return {"message": "Message saved to the database!"}
@app.get("/messages")
def get_messages():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    # Fetch everything from the messages table
    cursor.execute("SELECT name, content FROM messages")
    rows = cursor.fetchall()
    conn.close()
    
    # Format the data into a list of dictionaries for the Frontend
    return [{"name": row[0], "message": row[1]} for row in rows]