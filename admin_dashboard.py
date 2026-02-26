import streamlit as st
import sqlite3
import pandas as pd

# Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="Smart City Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart City Admin Dashboard")
st.markdown("Monitor and manage city information records.")

st.divider()

# Sidebar
st.sidebar.title("📁 Navigation")
menu = st.sidebar.selectbox(
    "Select Dataset",
    ["Hospitals", "Government Offices", "Tourist Places", "Utilities"]
)

# Database Connection
try:
    conn = sqlite3.connect("data/city_database.db")
    cursor = conn.cursor()
except Exception as e:
    st.error(f"Database connection failed: {e}")

df = None  # Initialize df

# Load Data Based on Selection
if menu == "Hospitals":
    df = pd.read_sql_query("SELECT * FROM hospitals", conn)

elif menu == "Government Offices":
    df = pd.read_sql_query("SELECT * FROM government_offices", conn)

elif menu == "Tourist Places":
    df = pd.read_sql_query("SELECT * FROM tourist_places", conn)

elif menu == "Utilities":
    df = pd.read_sql_query("SELECT * FROM utilities", conn)

# Display Data
if df is not None:
    st.subheader(f"📌 {menu} Data")
    st.write("Total Records:", len(df))
    st.dataframe(df, use_container_width=True)

conn.close()