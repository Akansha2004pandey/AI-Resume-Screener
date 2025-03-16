import streamlit as st
import pdfplumber
import docx
import os
import base64
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from auth import login_user, signup_user, is_authenticated

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="AI Resume Screener", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = is_authenticated()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def extract_text_from_pdf(uploaded_file):
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return None

def extract_text_from_docx(uploaded_file):
    if uploaded_file:
        doc = docx.Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])
    return None

def ask_gemini(resume_text, user_question):
    try:
        prompt = f"""
        Below is the resume text. Based on this resume, answer the following question:
        
        Resume Text:
        {resume_text}
        
        Question:
        {user_question}
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        st.warning(f"Error communicating with Gemini: {e}")
        return "Sorry, I couldn't generate a response. Please try again."

def auth_system():
    st.sidebar.title("🔐 Authentication")
    auth_option = st.sidebar.radio("Choose Option", ["Login", "Sign Up"])
    if auth_option == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if login_user(username, password):
                st.session_state["authenticated"] = True
                st.session_state.chat_history = []  # Clear chat on new login
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password")
    elif auth_option == "Sign Up":
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        role = st.sidebar.text_input("Role")
        if st.sidebar.button("Sign Up"):
            if signup_user(new_username, new_password, role):
                st.sidebar.success("Account created! Please log in.")
            else:
                st.sidebar.error("Username already exists.")

if not st.session_state["authenticated"]:
    auth_system()
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.session_state.chat_history = []  # Clear chat on logout
    st.experimental_rerun()

st.sidebar.title("🔍 AI Resume Screener")
menu = st.sidebar.radio("Go to", ["🏠 Home","📊 Resume Scoring", "🤖 AI Resume Chatbot"])
if menu == "🏠 Home":
    st.title("🏠 Welcome to AI Resume Screener!")
    st.write("""
        - 📊 **Resume Scoring:** Upload your resume & job description to get a match score.
        - 🤖 **AI Resume Chatbot:** Ask AI for resume improvement tips.
        - 🚀 **Smart Hiring:** Save time for both recruiters & job seekers!
    """)


elif menu == "📊 Resume Scoring":
    st.title("📊 Resume Scoring")

    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste Job Description Here")

    if st.button("Extract Text & Score Resume"):
        if uploaded_file and job_description:
            text = extract_text_from_pdf(uploaded_file) if uploaded_file.type == "application/pdf" else extract_text_from_docx(uploaded_file)

            if text:
                resume_str, job_desc_str, missing_suggestions = structure_with_gemini(text, job_description)
                percentage = compute_similarity(resume_str, job_desc_str)
                profile_strength, badge_class, icon = get_profile_strength(percentage)
            
                st.markdown(f"<h3 style='text-align:center; color:{'green' if badge_class == 'badge-success' else 'orange' if badge_class == 'badge-warning' else 'red'};'>Match Score: {percentage}% </h3>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align:center; color:{'green' if badge_class == 'badge-success' else 'orange' if badge_class == 'badge-warning' else 'red'};'>Profile Strength: {icon} {profile_strength}</h4>", unsafe_allow_html=True)

                st.write("### Extracted and Structured Resume Text:")
                st.write(resume_str)
                st.write("### Structured Job Description Text:")
                st.write(job_desc_str)

                # Display Missing Suggestions Section
                st.markdown(f"<h4 style='color:#4CAF50;'>💡 Suggested Improvements:</h4>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color:#f8f8f8; padding:10px; border-radius:5px; box-shadow:0 2px 5px rgba(0, 0, 0, 0.1);'>{missing_suggestions}</div>", unsafe_allow_html=True)
            else:
                st.warning("Could not extract text from the file. Please upload a valid PDF or DOCX.")
        else:
            st.warning("Please upload a resume and enter a job description before clicking submit.")
            
elif menu == "🤖 AI Resume Chatbot":
    st.title("🤖 AI Resume Chatbot")
    uploaded_file = st.file_uploader("Upload Resume for AI Chatbot", type=["pdf", "docx"])
    resume_text = ""
    
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)
        
        if resume_text:
            st.write("### Resume Preview:")
            pdf_base64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
            st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500" type="application/pdf"></iframe>', unsafe_allow_html=True)
        else:
            st.warning("Could not extract text from the resume.")
    
    user_question = st.text_input("Ask a question about the resume:")
    
    if user_question and resume_text:
        gemini_response = ask_gemini(resume_text, user_question)
        st.session_state.chat_history.append({"user": user_question, "gemini": gemini_response})
    
    if st.button("Delete Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.markdown(f"<div style='background-color:#e1f5fe; padding:10px; border-radius:20px; margin-bottom:10px; max-width:80%; margin-left:auto; text-align:right;'><strong>👤 You:</strong> {chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color:#f1f8e9; padding:10px; border-radius:20px; margin-bottom:10px; max-width:80%; margin-right:auto; text-align:left;'><strong>🤖 AI:</strong> {chat['gemini']}</div>", unsafe_allow_html=True)
