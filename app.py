import streamlit as st
from duckduckgo_search import DDGS
import subprocess
import PyPDF2
import difflib

# ===== PHOENIX BRAND =====
st.set_page_config(page_title="Phoenix AI", page_icon="🔥")
st.title("🐦‍🔥 PHOENIX AI")
st.write("Developed by red_phoenix11 • All Subjects • Any Doubt")

# ===== FUNCTIONS =====

# 1️⃣ Typo correction function
def correct_spelling(user_input, common_words=None):
    if not common_words:
        common_words = [
            "mathematics", "physics", "chemistry", "biology", "thermodynamics",
            "python", "javascript", "java", "programming", "engineering",
            "study", "career", "life", "tech", "ai", "machine learning",
            "pdf", "loop", "function", "array", "algorithm", "toc", "water"
        ]
    words = user_input.split()
    corrected = []
    for w in words:
        match = difflib.get_close_matches(w, common_words, n=1, cutoff=0.75)
        if match:
            corrected.append(match[0])
        else:
            corrected.append(w)
    return " ".join(corrected)

# 2️⃣ Web search
def web_search(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(r["body"])
    return "\n".join(results)

# 3️⃣ Ollama AI query
def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

# 4️⃣ PDF reader
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ===== INPUT AREA =====
option = st.selectbox(
    "Choose Mode",
    ["Ask Anything", "Web Search + AI", "PDF Doubt"]
)

question = st.text_area("Enter your doubt / question (Spelling mistakes okay!)")

uploaded = st.file_uploader("Upload PDF (optional)")

# ===== PROCESS =====
if st.button("ASK PHOENIX 🔥"):

    if not question.strip():
        st.warning("Please enter a question first!")
    else:
        # Step 1: Correct spelling
        clean_question = correct_spelling(question.lower())

        # Step 2: Initialize context
        context = ""

        if option == "Web Search + AI":
            st.info("Searching the web...")
            context += web_search(clean_question)

        if uploaded:
            context += "\nPDF CONTENT:\n" + read_pdf(uploaded)

        # Step 3: Final AI prompt
        final_prompt = f"""
You are PHOENIX AI developed by red_phoenix11.
You are friendly, smart, and can answer any doubt: study, life, tech, coding, or PDF content.

User Question:
{clean_question}

Context:
{context}

Rules:
- Answer in simple language, give examples
- If web/PDF context available, use it
- Correct spelling mistakes automatically
- Support English, Tamil, and mixed language (Tanglish)
"""

        # Step 4: AI response
        with st.spinner("Phoenix thinking... 🔥"):
            answer = ask_ollama(final_prompt)

        st.subheader("🔥 Phoenix Reply")
        st.write(answer)

# Footer
st.markdown("---")
st.caption("Phoenix AI • All Subject • All Life • Any Doubt Solver")

