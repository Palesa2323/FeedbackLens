import matplotlib.pyplot as plt


def create_sentiment_chart(results_df, theme=None):
    sentiment_counts = results_df["Sentiment"].value_counts()

    sentiments = ["Positive", "Negative", "Neutral"]

    counts = [
        sentiment_counts.get(sentiment, 0)
        for sentiment in sentiments
    ]

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Use standard colours when no pastel theme is selected
    if theme is None:
        chart_colors = [
            "#6BCB77",
            "#FF6B6B",
            "#FFB84D"
        ]
    else:
        chart_colors = [
            theme["positive"],
            theme["negative"],
            theme["neutral"]
        ]

    bars = ax.bar(
        sentiments,
        counts,
        color=chart_colors,
        width=0.55
    )

    # Add values above each bar
    for bar in bars:
        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    ax.set_title(
        "Sentiment Distribution",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        "Sentiment",
        fontsize=11
    )

    ax.set_ylabel(
        "Number of Feedback Entries",
        fontsize=11
    )

    # Remove unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add a subtle grid
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    fig.tight_layout()

    return fig