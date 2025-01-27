import streamlit as st
from project import *

def main_page():
    api = "https://newsnow.p.rapidapi.com/newsv2"

    buff, col, _ = st.columns([0.00001, 2, 7])  # Adjust ratios as needed
    api_key = col.text_input(
        "Enter RapidAPI NewsNow API Key",
        placeholder="API Key",
        label_visibility="visible",
        help="By default will use a secret API key with limited fetches"
    )
    if api_key == "":
        api_key = api_key = st.secrets["api"]["key"]

    buff, col, _ = st.columns([0.00001, 2, 7])  # Adjust ratios as needed
    company = col.text_input(
        "Search for company",
        key="search",
        placeholder="Enter company name",
        label_visibility="visible",
    )

    buff, col, _ = st.columns([0.00001, 2, 10])  # Adjust ratios as needed

    # Only allow the button to be pressed if company name is not empty
    if company:  # Checks if company name is not empty
        if col.button("Get Sentiment Value"):
            try:
                response = fetch_documents(api, company, api_key)
                news_list = process_data(response)
                documents, titles = organize_data(news_list)
                results, sentiment = calculate_polarity(documents, titles)
                
                # Display sentiment result
                col.markdown("<br>", unsafe_allow_html=True)
                col.write(f'<p style="font-size: 30px; white-space: nowrap;">Overall Sentiment: {sentiment:.2f}</p>', unsafe_allow_html=True)

                # Display articles
                col.write('<p style="font-size: 20px;">Articles Used:</p>', unsafe_allow_html=True)
                for title, url, sentiment_value in results:
                    # Create a hyperlinked title and display sentiment value
                    col.markdown(
                        f"""
                        <ul>
                            <li style='white-space: nowrap;'>
                                <a href='{url}' target='_blank' style='text-decoration: none; color: #0366d6; font-weight: bold;'>{title}</a>
                            </li>
                            <ul style='padding-left: 20px;'>
                                <li>Sentiment value: {sentiment_value:.2f}</li>
                            </ul>
                        </ul>
                        """,
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                # Custom error message
                col.write('<p style="color: red; font-size: 16px;">Daily API used or Wrong API key</p>', unsafe_allow_html=True)
                # Optionally log the error for debugging
                #st.error(f"Error details: {str(e)}")
    else:
        col.write('<p style="white-space: nowrap;">Please enter a company name to fetch the sentiment.</p>', unsafe_allow_html=True)
