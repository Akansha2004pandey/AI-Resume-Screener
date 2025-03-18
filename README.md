# AI Resume Screener & Builder

## 🚀 Overview
AI Resume Screener & Builder is an intelligent system designed to **analyze, enhance, and generate resumes** using AI. It automates the resume screening process for recruiters while helping job seekers optimize their resumes with AI-driven feedback and **LaTeX-powered resume building.**

## ✨ Features

### 🎯 **For Job Seekers**
- **AI Resume Scoring**: Upload a resume (PDF/DOCX) and get a **match score** based on job descriptions.
- **Resume Optimization**: AI suggests **missing skills, improvements, and formatting fixes**.
- **AI Chatbot for Resume Guidance**: Get **personalized career advice & resume improvement tips**.
- **AI-Powered Resume Builder**:
  - Generate **LaTeX-based resumes** with AI.
  - Built-in **code editor** for real-time LaTeX editing.
  - **Gemini API** generates resume content dynamically.

### 🏢 **For Recruiters**
- **Smart Resume Filtering**: AI **ranks & shortlists resumes** based on job descriptions.
- **Bias-Free Hiring**: AI detects **biased language & anonymizes resumes**.
- **Candidate Comparison Tool**: Compare multiple resumes side-by-side.
- **Automated Job Posting Suggestions**: AI suggests **ideal job postings** based on resume trends.

## 🔧 Tech Stack
- **Frontend:** Streamlit (for AI interaction UI)
- **AI Models:**
  - **Gemini API** (for resume structuring, suggestions, chat, & generation)
  - **Sentence Transformer (`all-MiniLM-L6-v2`)** for resume-job matching
- **Database:** Firebase (for Authentication & Chat History Storage)
- **Document Processing:** pdfplumber, docx2txt, LaTeX for structured resume formatting
- **Code Editor:** Monaco Editor (for live LaTeX-based resume editing)

## ⚙️ How It Works
1. **User uploads a resume** (PDF/DOCX)
2. **AI extracts key details** (Skills, Experience, etc.)
3. **Job description is provided** for comparison
4. **AI calculates match score** and suggests improvements
5. **AI Chatbot** provides career guidance & resume optimization
6. **AI Resume Builder** allows users to generate resumes using **LaTeX & Gemini API**
7. **Recruiters can filter, analyze, and compare resumes** efficiently

## 📌 Installation & Setup

### Prerequisites
- Python 3.8+
- Firebase Account (for Authentication & Storage)
- Cloudinary API (for Resume PDF storage, if needed)

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/Akansha2004pandey/ai-resume-screener.git
cd ai-resume-screener

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Environment Variables
Create a `.env` file and add the following credentials:
```env
FIREBASE_API_KEY=your_firebase_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## 🛠 Future Enhancements
- ✅ **ATS Integration**: Connect with **LinkedIn, Workday, Greenhouse**.
- ✅ **Custom Resume Templates**: AI-generated **resume templates based on job roles**.
- ✅ **Multi-language Resume Analysis**: Support for multiple languages.
- ✅ **Real-time Resume Collaboration**: Allow **recruiters & job seekers** to edit resumes together.

## 📜 License
This project is **open-source** under the MIT License.

## 📞 Contact
For any queries or collaboration:
📧 **Email:** akanshaoptimist@gmail.com  
🌐 **GitHub:** [Akansha2004pandey](https://github.com/Akansha2004pandey)

---
💡 **Empowering Careers with AI!** 🚀
