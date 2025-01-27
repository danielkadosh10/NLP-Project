import streamlit as st
from main_page import main_page
import nltk

def main():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded",
                       page_title="Stock Sentiment Analysis Scoring", page_icon="📈")
    st.title("Stock Review Sentiment Analysis")
    
    main_page()

if __name__ == "__main__":
    nltk.download('punkt_tab')
    nltk.download('vader_lexicon')
    
    main()
