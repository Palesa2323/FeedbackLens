import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sentiment import analyze_sentiment

#configuring the page layout and title
st.set_page_config(
    page_title="FeedbackLens - Sentiment Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)

# title of the web application
st.title("FeedbackLens - Sentiment Analysis") # st = streamlit
st.subheader("Analyze the sentiment of your feedback data")
st.write(
    "Analyze feedback, identify sentiment patterns, and generate useful insights to improve your services. Upload your feedback data in CSV format and let FeedbackLens do the rest!"
)

def load_data():
    return pd.read_csv("data/feedback_data.csv")

results = [] #analyzing sentiment

for feedback in load_data()["Feedback"]:
    sentiment, score = analyze_sentiment(feedback)
    
    results.append({
        "Feedback": feedback,
        "Sentiment": sentiment,
         "Score": score
    })
    
results_df = pd.DataFrame(results)

sentiment_counts = results_df["Sentiment"].value_counts() # calculate sentiment counts 

positive_count = sentiment_counts.get("Positive", 0)
negative_count = sentiment_counts.get("Negative", 0)
neutral_count = sentiment_counts.get("Neutral", 0)

total_reviews = len(results_df) # calculate total number of reviews

positive_percentage = (positive_count / total_reviews) * 100 
negative_percentage = (negative_count / total_reviews) * 100 
neutral_percentage = (neutral_count / total_reviews) * 100 