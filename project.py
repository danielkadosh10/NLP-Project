import requests
import requests
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer



# Purpose: Fetch the documents of a specific company
# Inputs:
#   api - the api link
#   company - the company name we want to fetch
def fetch_documents(api, company, X_RapidAPI_Key):
    payload = {
        "query": company,
        "time_bounded": True,
        "from_date": "01/02/2024",
        "to_date": "03/06/2024",
        "location": "us",
        "language": "en",
        "page": 1
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": X_RapidAPI_Key,
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    responses = []
    for i in range(1, 4):
        temp_payload = payload
        temp_payload['page'] = i
        responses.append(requests.post(api, json=temp_payload, headers=headers))

    response = requests.post(api, json=payload, headers=headers)
    return response


# Purpose: Process the data and fetch relevent info
# Inputs:
#   response - The response from the request to RapidAPI
def process_data(response):
    data = response.json()
    news_list = None

    if 'news' in data:
        news_list = data['news']
        for news_item in news_list:
            title = news_item['title']
            top_image = news_item.get('top_image', 'No top image found')
            images = news_item.get('images', [])
            about = news_item.get('short_description')
            url = news_item.get('url')
            text = news_item.get('text')

            print("Title:", title)
            #print("Top Image:", top_image)
            #print("Additional Images:", images)
            print("About: ", about)
            print("URL: ", url)
            # print("TXT: ", text)
            print("-------------")
    else:
        print("No news found in the response.")

    return news_list


# Purpose: Organize the data into
# Inputs:
#   news_list - The list of news articles
def organize_data(news_list):
    documents = {}
    titles = []

    for news_item in news_list:
        title = news_item['title']
        titles.append(title)
        txt = news_item['text']
        url = news_item.get('url')

        # since url unique and only once, intialize directly
        documents[url] = {'paragraphs': txt.split("\n\n"), 'sentences': []}

        for paragraph in documents[url]['paragraphs']:
            documents[url]['sentences'].append(tokenize.sent_tokenize(paragraph))

    return documents, titles


# Purpose: Print the paragraph and sentences 
# Inputs:
#   - documents - List of documents to print info
def print_docments(documents):
# for every article in document, viewing format (5 paragraphs, 5 sentences per paragraph for view simplicity)
    for url in documents:
        print(url)
        for i, paragraph in enumerate(documents[url]['paragraphs'][:5]):
            print("\t", "Paragraph ->", paragraph)
            print("\t\t", "Sentences ->")
            for sentence in documents[url]['sentences'][i]:
                print("\t\t", sentence.strip())

        print("-"*80)


# Purpose: Calculate the polarity of the fetched documents
# Inputs:
#   documents - List of documents to calculate polarity
def calculate_polarity(documents, titles):
    results = []

    sid = SentimentIntensityAnalyzer()
    sentiment = [0, 0]
    index = 0

    for url in documents:
        document_sentiments = []

        for i, paragraph in enumerate(documents[url]['paragraphs']):
            paragraph_sentiments = [] # stores sentiment of every sentence in the paragraph

            for sentence in documents[url]['sentences'][i]:
                # calculate sentiment polarity of the sentence
                sentence_sentiment_score = sid.polarity_scores(sentence.strip())
                compound_score = sentence_sentiment_score['compound']
                paragraph_sentiments.append(compound_score)

            # calculate avg sentiment polarity for the paragraph
            if paragraph_sentiments:
                paragraph_sentiment = sum(paragraph_sentiments) / len(paragraph_sentiments)
                document_sentiments.append(paragraph_sentiment)

        if document_sentiments:
            document_sentiment = sum(document_sentiments) / len(document_sentiments)
            print(f"Document URL: {url}")
            print(f"Sentiment: {document_sentiment}")

            results.append((titles[index], url, document_sentiment))
            sentiment[0] += document_sentiment
            sentiment[1] += 1

            index += 1
    
    print(f"Overall Sentiment: {sentiment[0]/sentiment[1]}")

    return results, sentiment[0]/sentiment[1]



if __name__ == "__main__":
    # Init nltk
    # nltk.download('punkt_tab')
    # nltk.download('vader_lexicon')
    
    # RapidAPI NewsNow
    X_RapidAPI_Key='f068e1ac87mshb80d32477a67206p129389jsn3f3e23e0ecde'
    api = "https://newsnow.p.rapidapi.com/newsv2"
    company = "Nvidia"
    response = fetch_documents(api, company, X_RapidAPI_Key)
    news_list = process_data(response)
    documents, titles = organize_data(news_list)
    # print_docments(documents)
    calculate_polarity(documents, titles)



