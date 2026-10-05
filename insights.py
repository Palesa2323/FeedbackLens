def generate_insights(summary):
    insights = []

    # Generate insights based on sentiment percentages
    if summary["positive_percentage"] > 50:
        insights.append("The majority of feedback is positive. Keep up the good work!")

    if summary["negative_percentage"] > 10:
        insights.append(
            f"There were {summary['negative_count']} negative feedback entries. Consider addressing the concerns raised."
        )

    if summary["neutral_percentage"] > 20:
        insights.append(
            "A large amount of feedback is neutral. Explore ways to engage users more effectively."
        )

    return insights