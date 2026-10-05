from collections import Counter


STOP_WORDS = {"the", "a", "an", "and", "or", "but", "to", "of",
    "in", "on", "for", "with", "was", "were", "is", "are",
    "i", "it", "this", "that", "my", "very", "some", "be",
    "more", "than", "so", "too", "could", "would"}

DESCRIPTIVE_WORDS = {
    "excellent", "informative", "helpful", "clear", "useful",
    "easy", "practical", "good", "great", "interesting",
    "interactive", "confusing", "boring", "difficult",
    "hard", "disappointed", "poor", "long", "slow",
    "technical", "crashing", "frustrating", "valuable",
    "enjoyable", "positive", "negative"
}

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
        data = results_df[
            results_df["Sentiment"] == sentiment
        ]["Feedback"]
    else:
        data = results_df["Feedback"]

    words = []

    for feedback_text in data:
        if not isinstance(feedback_text, str):
            continue

        for word in feedback_text.lower().split():
            word = word.strip(".,!?")

            if word in DESCRIPTIVE_WORDS:
                words.append(word)

    word_counts = Counter(words)

    return word_counts.most_common(top_n)

def generate_report_insights(summary, results_df):
    insights = []
    
    # overall sentiment insights
    if summary["positive_percentage"] > 50:
        insights.append(f" Positive feedback made up {summary['positive_percentage']:.1f}% of total feedback. This indicates a generally positive sentiment among users.")
       
    elif summary["negative_percentage"] > 50:
        insights.append(f" Negative feedback made up {summary['negative_percentage']:.1f}% of total feedback. This indicates a generally negative sentiment among users.")
        
    else:
        insights.append(
            "The feedback shows a mixed sentiment pattern, with no single sentiment "
            "category accounting for more than half of the responses."
        )

    # Negative feedback insight
    if summary["negative_count"] > 0:
        negative_words = find_common_words(results_df, "Negative")

        words = ", ".join(
            word for word, count in negative_words[:5]
        )

        insights.append(
            f"Negative feedback accounted for {summary['negative_percentage']:.1f}% "
            f"of responses. Common terms included: {words}."
        )

    # Neutral feedback insight
    if summary["neutral_count"] > 0:
        insights.append(
            f"Neutral feedback accounted for {summary['neutral_percentage']:.1f}% "
            "of responses, suggesting that some learners had mixed or moderate views."
        )

    return insights

def generate_recommendations(summary, results_df):
    recommendations = []

    negative_words = find_common_words(
        results_df,
        "Negative"
    )

    negative_terms = [
        word for word, count in negative_words
    ]

    if "boring" in negative_terms:
        recommendations.append(
            "Increase learner engagement by adding more interactive "
            "activities and practical exercises."
        )

    if "confusing" in negative_terms or "difficult" in negative_terms:
        recommendations.append(
            "Review difficult or confusing topics and provide clearer "
            "instructions, explanations, and examples."
        )

    if "long" in negative_terms:
        recommendations.append(
            "Consider breaking longer sessions into shorter sections "
            "with regular activities or breaks."
        )

    if "technical" in negative_terms or "crashing" in negative_terms:
        recommendations.append(
            "Investigate technical issues with the learning platform "
            "to improve the overall user experience."
        )

    if summary["positive_percentage"] > 50:
        recommendations.append(
            "Continue using the teaching approaches and practical "
            "activities that contributed to the positive feedback."
        )

    if not recommendations:
        recommendations.append(
            "Continue monitoring learner feedback to identify emerging "
            "areas for improvement."
        )

    return recommendations

def create_report_data(summary, results_df):
    report_data = {
        "total_feedback": summary["total_reviews"],
        "positive_count": summary["positive_count"],
        "negative_count": summary["negative_count"],
        "neutral_count": summary["neutral_count"],
        "positive_percentage": summary["positive_percentage"],
        "negative_percentage": summary["negative_percentage"],
        "neutral_percentage": summary["neutral_percentage"],
        "positive_words": find_common_words(
            results_df,
            "Positive",
            top_n=5
        ),
        "negative_words": find_common_words(
            results_df,
            "Negative",
            top_n=5
        ),
        "neutral_words": find_common_words(
            results_df,
            "Neutral",
            top_n=5
        ),
        "insights": generate_report_insights(
            summary,
            results_df
        ),
        "recommendations": generate_recommendations(
            summary,
            results_df
        )
    }

    return report_data