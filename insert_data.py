import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("data/city_database.db")
cursor = conn.cursor()

# Load CSV files
hospitals = pd.read_csv("data/guwahati_hospitals.csv")
govt = pd.read_csv("data/guwahati_govt_offices_proper.csv")
tourist = pd.read_csv("data/guwahati_tourist_and_parks.csv")
utilities = pd.read_csv("data/guwahati_city_utilities.csv")

# Insert Hospitals
for _, row in hospitals.iterrows():
    cursor.execute("""
    INSERT INTO hospitals 
    (name, area, contact, opening_time, closing_time, emergency_available, image_path, google_map_link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row.get("name", ""),
        row.get("area", ""),
        row.get("contact", ""),
        "00:00",
        "23:59",
        "Yes",
        f"images/hospitals/{row.get('name','').replace(' ','_')}.jpg",
        f"https://www.google.com/maps?q={row.get('name','')}+Guwahati"
    ))

# Insert Government Offices
for _, row in govt.iterrows():
    cursor.execute("""
    INSERT INTO government_offices 
    (office_name, department, address, contact, opening_time, closing_time, image_path, google_map_link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row.get("office_name", ""),
        row.get("department", ""),
        row.get("address", ""),
        row.get("contact", ""),
        "10:00 AM",
        "5:00 PM",
        f"images/govt_offices/{row.get('office_name','').replace(' ','_')}.jpg",
        f"https://www.google.com/maps?q={row.get('office_name','')}+Guwahati"
    ))

# Insert Tourist Places
for _, row in tourist.iterrows():
    cursor.execute("""
    INSERT INTO tourist_places
    (name, type, location, timing, image_path, google_map_link)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row.get("name", ""),
        row.get("type", ""),
        row.get("location", ""),
        "9:00 AM - 6:00 PM",
        f"images/tourist/{row.get('name','').replace(' ','_')}.jpg",
        f"https://www.google.com/maps?q={row.get('name','')}+Guwahati"
    ))

# Insert Utilities
for _, row in utilities.iterrows():
    cursor.execute("""
    INSERT INTO utilities (service, helpline)
    VALUES (?, ?)
    """, (
        row.get("service", ""),
        row.get("helpline", "")
    ))

# Insert Emergency Contacts (Manual Add)
emergency_data = [
    ("Police", "100"),
    ("Ambulance", "108"),
    ("Fire", "101"),
    ("Women Helpline", "181"),
    ("Disaster Management", "1070")
]

for service, number in emergency_data:
    cursor.execute("""
    INSERT INTO emergency_contacts (service_name, helpline)
    VALUES (?, ?)
    """, (service, number))

conn.commit()
conn.close()

print("Data inserted successfully!")