
def generate_insights(summary):
    """Generate evidence-based insights from sentiment summary data."""

    insights = []

    total = summary["total_reviews"]
    positive = summary["positive_count"]
    negative = summary["negative_count"]
    neutral = summary["neutral_count"]

    if total == 0:
        return ["Upload feedback to discover sentiment patterns."]

    positive_pct = summary["positive_percentage"]
    negative_pct = summary["negative_percentage"]
    neutral_pct = summary["neutral_percentage"]

    # Identify the dominant sentiment
    sentiments = {
        "Positive": positive,
        "Negative": negative,
        "Neutral": neutral,
    }

    highest_count = max(sentiments.values())
    dominant = [
        name for name, count in sentiments.items()
        if count == highest_count
    ]

    if len(dominant) == 1:
        name = dominant[0]
        percentage = summary[f"{name.lower()}_percentage"]

        insights.append(
            f"{name} sentiment is the largest category, accounting "
            f"for {highest_count:,} of {total:,} responses "
            f"({percentage:.1f}%)."
        )
    else:
        tied_names = ", ".join(dominant)

        insights.append(
            f"Feedback is split across {tied_names}, with "
            f"{highest_count:,} responses in each category. "
            "There is no single dominant sentiment."
        )

    # Positive sentiment
    if positive_pct >= 70:
        insights.append(
            f"Strong positive feedback: {positive_pct:.1f}% "
            f"of responses ({positive:,}) were classified as positive. "
            "Review positive comments to identify strengths worth maintaining."
        )
    elif positive_pct > 50:
        insights.append(
            f"More than half of the feedback is positive "
            f"({positive_pct:.1f}%, or {positive:,} responses). "
            "Explore the positive comments to understand what is working well."
        )

    # Negative sentiment
    if negative_pct >= 30:
        insights.append(
            f"Negative sentiment is substantial at {negative_pct:.1f}% "
            f"({negative:,} responses). Prioritise reviewing these comments "
            "to identify recurring concerns."
        )
    elif negative_pct > 10:
        insights.append(
            f"{negative:,} responses ({negative_pct:.1f}%) were classified "
            "as negative. Review the comments to identify potential "
            "areas for improvement."
        )

    # Neutral sentiment
    if neutral_pct >= 40:
        insights.append(
            f"Neutral sentiment accounts for {neutral_pct:.1f}% "
            f"({neutral:,} responses). These comments may contain factual "
            "observations or limited emotional language, so review their "
            "content before drawing conclusions."
        )
    elif neutral_pct > 20:
        insights.append(
            f"{neutral_pct:.1f}% of responses ({neutral:,}) were neutral. "
            "Review these responses for useful observations that may not "
            "express a strong positive or negative opinion."
        )

    if not insights:
        insights.append(
            "No strong sentiment pattern was identified by the current "
            "rules. Review the distribution and individual comments "
            "for additional context."
        )

    return insights
