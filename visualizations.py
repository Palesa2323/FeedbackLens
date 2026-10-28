
import matplotlib.pyplot as plt
import numpy as np


# --------------------------------------------------
# SHARED CHART STYLING
# --------------------------------------------------

BACKGROUND = "#FFFCFF"
TEXT_COLOR = "#655078"
MUTED_COLOR = "#8B7A96"
GRID_COLOR = "#E8DDED"

SENTIMENT_COLORS = {
    "Positive": "#B9A0D5",
    "Negative": "#E7A6B8",
    "Neutral": "#E8CC91",
}


def get_sentiment_data(results_df, theme=None):
    """Return sentiment labels, counts, and matching colours."""

    sentiments = ["Positive", "Negative", "Neutral"]
    sentiment_counts = results_df["Sentiment"].value_counts()

    counts = [
        int(sentiment_counts.get(sentiment, 0))
        for sentiment in sentiments
    ]

    if theme is None:
        colors = [SENTIMENT_COLORS[s] for s in sentiments]
    else:
        colors = [
            theme.get(s.lower(), SENTIMENT_COLORS[s])
            for s in sentiments
        ]

    return sentiments, counts, colors


def style_axes(ax):
    """Apply consistent styling to chart axes."""

    ax.set_facecolor(BACKGROUND)
    ax.tick_params(colors=MUTED_COLOR, labelsize=10)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.7,
        color=GRID_COLOR,
        alpha=0.8,
    )

    ax.set_axisbelow(True)


# --------------------------------------------------
# 1. SENTIMENT DISTRIBUTION BAR CHART
# --------------------------------------------------

def create_sentiment_chart(results_df, theme=None):
    sentiments, counts, colors = get_sentiment_data(
        results_df, theme
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BACKGROUND)

    bars = ax.bar(
        sentiments,
        counts,
        color=colors,
        width=0.55,
        edgecolor=BACKGROUND,
        linewidth=1.5,
    )

    for bar, count in zip(bars, counts):
        ax.annotate(
            str(count),
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=11,
            fontweight="bold",
            color=TEXT_COLOR,
        )

    ax.set_title(
        "Sentiment Distribution",
        fontsize=15,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=18,
    )
    ax.set_ylabel("Number of responses", color=MUTED_COLOR)

    style_axes(ax)
    ax.margins(y=0.18)

    fig.tight_layout()
    return fig


# --------------------------------------------------
# 2. SENTIMENT DONUT CHART
# --------------------------------------------------

def create_sentiment_donut(results_df, theme=None):
    sentiments, counts, colors = get_sentiment_data(
        results_df, theme
    )

    total = sum(counts)

    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    if total == 0:
        ax.text(
            0.5, 0.5, "No feedback to display",
            ha="center", va="center",
            color=MUTED_COLOR,
            fontsize=12,
            transform=ax.transAxes,
        )
        ax.axis("off")
        fig.tight_layout()
        return fig

    wedges, _ = ax.pie(
        counts,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={
            "width": 0.34,
            "edgecolor": BACKGROUND,
            "linewidth": 3,
        },
    )

    ax.text(
        0, 0.08, f"{total:,}",
        ha="center", va="center",
        fontsize=24, fontweight="bold",
        color=TEXT_COLOR,
    )
    ax.text(
        0, -0.16, "Responses",
        ha="center", va="center",
        fontsize=10, color=MUTED_COLOR,
    )

    ax.legend(
        wedges,
        [
            f"{sentiment}  ·  {count:,} ({count / total:.1%})"
            for sentiment, count in zip(sentiments, counts)
        ],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.12),
        frameon=False,
        fontsize=9,
    )

    ax.set_title(
        "Sentiment at a Glance",
        fontsize=15,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=16,
    )

    fig.tight_layout()
    return fig


# --------------------------------------------------
# 3. HORIZONTAL SENTIMENT COMPARISON
# --------------------------------------------------

def create_sentiment_comparison(results_df, theme=None):
    sentiments, counts, colors = get_sentiment_data(
        results_df, theme
    )

    fig, ax = plt.subplots(figsize=(7, 3.8))
    fig.patch.set_facecolor(BACKGROUND)

    # Reverse the order so the first category appears at the top.
    sentiments = sentiments[::-1]
    counts = counts[::-1]
    colors = colors[::-1]

    bars = ax.barh(
        sentiments,
        counts,
        color=colors,
        height=0.52,
        edgecolor=BACKGROUND,
        linewidth=1.5,
    )

    for bar, count in zip(bars, counts):
        ax.annotate(
            f"{count:,}",
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            xytext=(8, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=TEXT_COLOR,
        )

    ax.set_title(
        "Compare Sentiment Categories",
        fontsize=14,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=16,
    )
    ax.set_xlabel("Number of responses", color=MUTED_COLOR)
    ax.grid(axis="x", linestyle="--", alpha=0.25, color=GRID_COLOR)
    ax.grid(axis="y", visible=False)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(colors=MUTED_COLOR)
    ax.margins(x=0.18)

    fig.tight_layout()
    return fig


# --------------------------------------------------
# 4. COMPOUND SENTIMENT SCORE DISTRIBUTION
# --------------------------------------------------

def create_score_distribution(results_df):
    score_column = "compound"

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    if score_column not in results_df.columns:
        ax.text(
            0.5, 0.5,
            "Compound scores are not available in this dataset.",
            ha="center", va="center",
            color=MUTED_COLOR,
            transform=ax.transAxes,
            fontsize=11,
        )
        ax.axis("off")
        fig.tight_layout()
        return fig

    scores = results_df[score_column].dropna()

    if scores.empty:
        ax.text(
            0.5, 0.5, "No sentiment scores to display",
            ha="center", va="center",
            color=MUTED_COLOR,
            transform=ax.transAxes,
            fontsize=11,
        )
        ax.axis("off")
        fig.tight_layout()
        return fig

    ax.hist(
        scores,
        bins=np.linspace(-1, 1, 21),
        color="#C9B4E3",
        edgecolor=BACKGROUND,
        linewidth=1.2,
    )

    ax.axvline(
        -0.05, color="#D48CA2",
        linestyle="--", linewidth=1.5,
        label="Negative threshold",
    )
    ax.axvline(
        0.05, color="#A18AC0",
        linestyle="--", linewidth=1.5,
        label="Positive threshold",
    )
    ax.axvline(
        0, color=MUTED_COLOR,
        linestyle=":", linewidth=1,
    )

    ax.set_title(
        "How Strong Is the Sentiment?",
        fontsize=15,
        fontweight="bold",
        color=TEXT_COLOR,
        pad=16,
    )
    ax.set_xlabel("VADER compound score", color=MUTED_COLOR)
    ax.set_ylabel("Number of responses", color=MUTED_COLOR)
    ax.set_xlim(-1, 1)

    style_axes(ax)
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    return fig
