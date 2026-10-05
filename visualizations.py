import matplotlib.pyplot as plt

def create_sentiment_chart(results_df):
    # Count the number of feedbacks for each sentiment category
    sentiment_counts = results_df["Sentiment"].value_counts()

    fig, ax = plt.subplots()
    # Create a bar chart for sentiment counts
    sentiment_counts.plot(
        kind="bar",
        ax=ax, 
        )
    
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Feedbacks")
    
    return fig