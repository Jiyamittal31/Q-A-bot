import streamlit as st
from utils import load_file
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

st.set_page_config(page_title="StudyMate", layout="wide")

# Tabs
tabs = st.tabs(["📚 Q&A", "📝 Summarizer", "🎯 Quiz Generator", "📅 Study Planner"])

# Shared storage
if "documents" not in st.session_state:
    st.session_state.documents = ""

with tabs[0]:  # Q&A
    st.header("📚 Ask Questions from Your Notes")
    uploaded = st.file_uploader("Upload your notes (PDF/DOCX/TXT)", type=["pdf","docx","txt"])
    if uploaded:
        st.session_state.documents = load_file(uploaded)
        st.success("File loaded successfully!")
    
    question = st.text_input("Ask a question:")
    if question and st.session_state.documents:
        qa = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        result = qa(question=question, context=st.session_state.documents)
        st.write(f"**Answer:** {result['answer']}")

#Summarizer        
with tabs[1]:
    st.header("📝 Summarizer")
    if st.session_state.documents:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        if st.button("Generate Summary"):
            summary = summarizer(st.session_state.documents[:1000], max_length=150, min_length=40, do_sample=False)
            st.write("### Summary:")
            st.write(summary[0]['summary_text'])
    else:
        st.info("Please upload notes in Q&A tab first.")

import random
#Quiz Generator
with tabs[2]:
    st.header("🎯 Quiz Generator")
    if st.session_state.documents:
        sentences = st.session_state.documents.split(".")
        sample_sentences = random.sample(sentences, min(5, len(sentences)))
        
        st.write("### Generated Questions:")
        for idx, sent in enumerate(sample_sentences, 1):
            st.write(f"Q{idx}: {sent.strip()} ... ?")
    else:
        st.info("Upload notes first.")

import datetime
#Study Planner
with tabs[3]:
    st.header("📅 Study Planner")
    exam_date = st.date_input("Select your exam date")
    if st.session_state.documents and exam_date:
        today = datetime.date.today()
        days_left = (exam_date - today).days
        word_count = len(st.session_state.documents.split())
        daily_goal = word_count // max(days_left, 1)
        st.success(f"You have {days_left} days left.")
        st.write(f"Suggested Daily Target: **{daily_goal} words/day**")

