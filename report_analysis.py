from collections import Counter

from streamlit import feedback

STOP_WORDS = {"the", "a", "an", "and", "or", "but", "to", "of",
    "in", "on", "for", "with", "was", "were", "is", "are",
    "i", "it", "this", "that", "my", "very", "some", "be",
    "more", "than", "so", "too", "could", "would"}

def analyze_sentiment_distribution(summary):
    return {
        "Positive": summary["positive_count"],
        "Negative": summary["negative_count"],
        "Neutral": summary["neutral_count"]
    }
    
def get_report_feedback(results_df):
    positive_feedback = results_df[results_df["Sentiment"] == "Positive"]
    negative_feedback = results_df[results_df["Sentiment"] == "Negative"]
    neutral_feedback = results_df[results_df["Sentiment"] == "Neutral"]

    return {
        "Positive": positive_feedback,
        "Negative": negative_feedback,
        "Neutral": neutral_feedback
    }
    
def find_common_words(results_df, sentiment=None, top_n=10):
    if sentiment:
        data = results_df[results_df["Sentiment"] == sentiment]["Feedback"]
    else:
        data = results_df["Feedback"]
        
    words = []
    
    for word in feedback.lower().split():
        word = word.strip(".,!?")
    
    if word not in STOP_WORDS:
        words.append(word)
        
    word_counts = Counter(words)
    return word_counts.most_common(10)

def generate_report_insights(summary, results_df):
    insights = []
    
    # overall sentiment insights
    if summary["positive_percentage"] > 50:
        insights.append("The majority of feedback is positive. Keep up the good work!")