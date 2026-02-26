import sqlite3

conn = sqlite3.connect("data/city_database.db")
cursor = conn.cursor()

# Hospitals Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    area TEXT,
    contact TEXT,
    opening_time TEXT,
    closing_time TEXT,
    emergency_available TEXT,
    image_path TEXT,
    google_map_link TEXT
)
""")

# Government Offices
cursor.execute("""
CREATE TABLE IF NOT EXISTS government_offices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    office_name TEXT,
    department TEXT,
    address TEXT,
    contact TEXT,
    opening_time TEXT,
    closing_time TEXT,
    image_path TEXT,
    google_map_link TEXT
)
""")

# Tourist Places
cursor.execute("""
CREATE TABLE IF NOT EXISTS tourist_places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type TEXT,
    location TEXT,
    timing TEXT,
    image_path TEXT,
    google_map_link TEXT
)
""")

# Utilities
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT,
    helpline TEXT
)
""")

# Emergency Contacts
cursor.execute("""
CREATE TABLE IF NOT EXISTS emergency_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT,
    helpline TEXT
)
""")

# Query Logs
cursor.execute("""
CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT,
    predicted_intent TEXT,
    language TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")