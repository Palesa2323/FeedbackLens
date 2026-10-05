from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from data_loader import load_data

def analyze_sentiment(text):
    #intialization of the SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    #calculates the polarity scores for the input text
    scores = analyzer.polarity_scores(text)

    #extract the overall composite sentiment score from the scores dictionary
    compound_score = scores["compound"]

    # Classify sentiment using standard VADER compound score thresholds
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, compound_score


if __name__ == "__main__":
    # Example usage
    test_text = "The training was excellent and very informative."
    # run the sentiment analysis function on the test text
    sentiment, score = analyze_sentiment(test_text)

    print(f"Sentiment: {sentiment}")
    print(f"Score: {score}")