import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase
import json

# ✅ Load Firebase Admin SDK Config (for Firestore & User Management)
with open("firebase_config.json") as f:
    firebase_admin_config = json.load(f)

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Load Pyrebase Config (for Authentication)
with open("pyrebase_config.json") as f:
    pyrebase_config = json.load(f)

firebase = pyrebase.initialize_app(pyrebase_config)
firebase_auth = firebase.auth()


# ✅ Signup Function
def signup_user(email, password, role):
    try:
        user = auth.create_user(email=email, password=password)  # Firebase Admin SDK
        user_id = user.uid

        db.collection("users").document(user_id).set({
            "email": email,
            "role": role
        })

        return user_id
    except Exception as e:
        st.error(f"Signup error: {e}")
        return None


# ✅ Login Function
def login_user(email, password):
    
    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)  # Pyrebase Auth
        user_id = user["localId"]  

        user_doc = db.collection("users").document(user_id).get()
        if user_doc.exists:
            return user, user_doc.to_dict()["role"]
        else:
            st.error("User role not found!")
            return None, None
    except Exception as e:
        st.error(f"Login error: {e}")
        return None, None


def is_authenticated():
    return "user" in st.session_state and st.session_state["user"] is not None 

# ✅ Logout Function
def logout():
    st.session_state["user"] = None
    st.session_state["role"] = None
