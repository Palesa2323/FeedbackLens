import pandas as pd

from data_loader import load_data
from sentiment import analyze_sentiment


def analyze_feedback(uploaded_file=None):
    data = load_data(uploaded_file)
    
    results = []

    # Analyze the sentiment of each feedback
    for feedback in data["feedback"]:
        sentiment, score = analyze_sentiment(feedback)

        results.append({
            "Feedback": feedback,
            "Sentiment": sentiment,
            "Score": score
        })

    results_df = pd.DataFrame(results)

    return results_df


def calculate_summary(results_df):
    # Calculate sentiment counts
    sentiment_counts = results_df["Sentiment"].value_counts()

    positive_count = sentiment_counts.get("Positive", 0)
    negative_count = sentiment_counts.get("Negative", 0)
    neutral_count = sentiment_counts.get("Neutral", 0)

    # Calculate total number of reviews
    total_reviews = len(results_df)

    # Calculate percentages
    positive_percentage = (positive_count / total_reviews) * 100
    negative_percentage = (negative_count / total_reviews) * 100
    neutral_percentage = (neutral_count / total_reviews) * 100

    return {
        "total_reviews": total_reviews,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "neutral_percentage": neutral_percentage
    }
    
def get_feedback_by_sentiment(results_df, sentiment):
    return results_df[results_df["Sentiment"] == sentiment]