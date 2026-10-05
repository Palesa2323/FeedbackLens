import pandas as pd

from data_loader import load_data
from sentiment import analyze_sentiment

def analyze_feedback():
    data = load_data()

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
