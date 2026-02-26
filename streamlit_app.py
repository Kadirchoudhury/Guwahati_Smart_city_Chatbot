# ==========================================
# IMPORT LIBRARIES
# ==========================================

import streamlit as st
import pandas as pd
import sqlite3
import joblib
import os

st.write("RUNNING CORRECT FILE ✅")

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Guwahati Smart City Assistant",
    page_icon="🏙️",
    layout="wide"
)

# ==========================================
# PATH SETTINGS
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model")
DB_PATH = os.path.join(BASE_DIR, "../data/city_database.db")

# ==========================================
# LOAD MODEL SAFELY
# ==========================================
try:

    model = joblib.load(os.path.join(MODEL_PATH, "model.pkl"))
    vectorizer = joblib.load(os.path.join(MODEL_PATH, "vectorizer.pkl"))
    label_encoder = joblib.load(os.path.join(MODEL_PATH, "label_encoder.pkl"))
    model_loaded = True
except Exception as e:
    model_loaded = False
    print("Model loading error:", e)
# ==========================================
# INTENT PREDICTION
# ==========================================
def predict_response(user_input):
    input_vector = vectorizer.transform([user_input])
    prediction = model.predict(input_vector)
    intent = label_encoder.inverse_transform(prediction)[0]
    return intent

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("🏙️ Smart City Navigation")
page = st.sidebar.selectbox(
    "Go to",
    ["Home", "Chatbot", "Analytics"]
)

# ==========================================
# HOME PAGE
# ==========================================
if page == "Home":
    st.title("🏙️ Guwahati Smart City System")
    st.markdown("### AI-Powered City Information Dashboard")
    st.write("""
    This system helps citizens access:
    - 🏥 Hospital Information
    - 🏢 Government Offices
    - 🏞 Tourist Places
    - ⚡ Utility Services
    """)
    st.success("Use the sidebar to start exploring.")

# ==========================================
# CHATBOT PAGE
# ==========================================
# ==========================================
# CHATBOT PAGE
# ==========================================
elif page == "Chatbot":

    st.title("🤖 Smart City Chatbot")
    st.markdown("Ask about hospitals, offices, tourist places, or utilities.")
    st.divider()

    if not model_loaded:
        st.error("⚠ Model files not found. Please check the model folder.")
    else:
        user_input = st.text_input("💬 Enter your query")

        if st.button("🔍 Get Information"):
            if user_input:

                intent = predict_response(user_input)

                conn = sqlite3.connect(DB_PATH)

                try:
                    # ----------------------------
                    # HOSPITAL
                    # ----------------------------
                    if intent == "find_hospital":
                        df = pd.read_sql_query(
                            "SELECT * FROM hospitals",
                            conn
                        )

                    # ----------------------------
                    # GOVERNMENT OFFICE
                    # ----------------------------
                    elif intent == "find_govt_office":
                        df = pd.read_sql_query(
                            "SELECT * FROM government_offices",
                            conn
                        )

                    # ----------------------------
                    # TOURIST PLACE
                    # ----------------------------
                    elif intent == "find_tourist_place":
                        df = pd.read_sql_query(
                            "SELECT * FROM tourist_places",
                            conn
                        )

                    # ----------------------------
                    # UTILITIES
                    # ----------------------------
                    elif intent == "find_utility":
                        df = pd.read_sql_query(
                            "SELECT * FROM utilities",
                            conn
                        )

                    else:
                        df = None

                except Exception as e:
                    st.error(f"Database error: {e}")
                    df = None

                conn.close()

                # ----------------------------
                # DISPLAY RESULT
                # ----------------------------
                if df is not None and not df.empty:
                    st.success("Here is the information:")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No data found in database.")

            else:
                st.warning("Please enter a query.")

# ==========================================
# ANALYTICS PAGE
# ==========================================
elif page == "Analytics":

    st.title("📊 Smart City Data Analytics")
    st.divider()

    conn = sqlite3.connect(DB_PATH)

    try:
        hospitals = pd.read_sql_query("SELECT COUNT(*) as total FROM hospitals", conn)
        offices = pd.read_sql_query("SELECT COUNT(*) as total FROM government_offices", conn)
        tourist = pd.read_sql_query("SELECT COUNT(*) as total FROM tourist_places", conn)
        utilities = pd.read_sql_query("SELECT COUNT(*) as total FROM utilities", conn)

        data_summary = pd.DataFrame({
            "Category": ["Hospitals", "Govt Offices", "Tourist Places", "Utilities"],
            "Count": [
                hospitals["total"][0],
                offices["total"][0],
                tourist["total"][0],
                utilities["total"][0]
            ]
        })

    except Exception as e:
        st.error(f"Database error: {e}")
        data_summary = None

    conn.close()

    if data_summary is not None:

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🏥 Hospitals", data_summary["Count"][0])
            st.metric("🏢 Govt Offices", data_summary["Count"][1])

        with col2:
            st.metric("🏞 Tourist Places", data_summary["Count"][2])
            st.metric("⚡ Utilities", data_summary["Count"][3])

        st.subheader("📈 Data Distribution")
        st.bar_chart(data_summary.set_index("Category"))