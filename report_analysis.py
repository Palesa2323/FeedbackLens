
import re
from collections import Counter


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "to", "of", "in", "on",
    "for", "with", "was", "were", "is", "are", "am", "be", "been",
    "being", "i", "it", "this", "that", "my", "we", "our", "you",
    "your", "they", "their", "he", "she", "them", "me", "us",
    "very", "some", "more", "than", "so", "too", "could", "would",
    "should", "can", "will", "just", "have", "has", "had", "do",
    "does", "did", "not", "no", "yes", "as", "at", "by", "from",
    "if", "then", "there", "here", "when", "what", "which", "who",
    "all", "any", "about", "also", "really", "because", "into",
    "its", "im", "ive", "weve", "dont", "didnt", "doesnt",
    "wasnt", "werent", "wouldnt", "couldnt", "shouldnt",
    "after", "before", "up", "down", "out", "over", "under",
    "get", "got", "make", "made", "thing", "things",
}

# Broad themes that can occur across industries.
ISSUE_THEMES = {
    "clarity": {
        "confusing", "unclear", "difficult", "complicated",
        "understand", "understanding", "instructions",
    },
    "service and support": {
        "service", "support", "staff", "rude", "unhelpful",
        "communication", "response", "responsive",
    },
    "technical reliability": {
        "technical", "crashing", "crash", "bug", "bugs",
        "error", "errors", "broken", "loading", "glitch",
    },
    "timing and delays": {
        "late", "delay", "delayed", "waiting", "wait",
        "slow", "long", "quickly",
    },
    "cost and value": {
        "expensive", "overpriced", "costly", "price",
        "pricing", "affordable", "value",
    },
    "quality and reliability": {
        "poor", "faulty", "defective", "damaged",
        "unreliable", "quality", "reliable",
    },
}

THEME_RECOMMENDATIONS = {
    "clarity": (
        "Review the comments mentioning confusion or difficulty. "
        "Simplify unclear instructions, explanations, or processes "
        "and test whether the revised version is easier to understand."
    ),
    "service and support": (
        "Review feedback about service and support. Identify recurring "
        "complaints about communication or assistance, then address "
        "the specific gaps found in the comments."
    ),
    "technical reliability": (
        "Investigate comments mentioning technical problems. Check for "
        "recurring errors, failures, or performance issues and verify "
        "whether corrective action resolves them."
    ),
    "timing and delays": (
        "Review comments about waiting times, delays, or slow processes. "
        "Identify where delays occur before deciding which process "
        "improvements are appropriate."
    ),
    "cost and value": (
        "Review feedback about pricing and value. Compare the concerns "
        "with the product or service offered before considering changes "
        "to pricing, communication, or value."
    ),
    "quality and reliability": (
        "Investigate comments about quality or reliability. Look for "
        "repeated defects or service failures and determine where "
        "quality checks or follow-up may help."
    ),
}


def analyze_sentiment_distribution(summary):
    return {
        "Positive": summary["positive_count"],
        "Negative": summary["negative_count"],
        "Neutral": summary["neutral_count"],
    }


def get_report_feedback(results_df):
    return {
        sentiment: results_df[
            results_df["Sentiment"] == sentiment
        ]
        for sentiment in ["Positive", "Negative", "Neutral"]
    }


def tokenize_feedback(feedback_text):
    """Extract readable words from a feedback comment."""

    if not isinstance(feedback_text, str):
        return []

    words = re.findall(r"[a-zA-Z][a-zA-Z'-]*", feedback_text.lower())

    return [
        word.strip("'-")
        for word in words
        if len(word.strip("'-")) > 2
        and word.strip("'-") not in STOP_WORDS
    ]


def find_common_words(results_df, sentiment=None, top_n=10):
    """Find frequent meaningful words across the selected feedback."""

    if "Feedback" not in results_df.columns:
        return []

    data = results_df

    if sentiment:
        data = data[data["Sentiment"] == sentiment]

    words = []

    for feedback_text in data["Feedback"]:
        words.extend(tokenize_feedback(feedback_text))

    return Counter(words).most_common(top_n)


def generate_report_insights(summary, results_df):
    """Create descriptive findings supported by the uploaded data."""

    insights = []

    total = summary["total_reviews"]

    if total == 0:
        return ["Upload feedback to generate a report."]

    positive_pct = summary["positive_percentage"]
    negative_pct = summary["negative_percentage"]
    neutral_pct = summary["neutral_percentage"]

    # Overall sentiment pattern
    if positive_pct > 50:
        insights.append(
            f"Positive sentiment represents {positive_pct:.1f}% "
            f"of the {total:,} responses "
            f"({summary['positive_count']:,} responses)."
        )
    elif negative_pct > 50:
        insights.append(
            f"Negative sentiment represents {negative_pct:.1f}% "
            f"of the {total:,} responses "
            f"({summary['negative_count']:,} responses)."
        )
    else:
        insights.append(
            "The feedback has a mixed sentiment distribution. "
            f"Positive: {positive_pct:.1f}%, negative: "
            f"{negative_pct:.1f}%, and neutral: {neutral_pct:.1f}%."
        )

    # Most frequent terms in negative feedback
    if summary["negative_count"] > 0:
        negative_words = find_common_words(
            results_df, "Negative", top_n=5
        )

        if negative_words:
            terms = ", ".join(
                f"{word} ({count})"
                for word, count in negative_words
            )
            insights.append(
                "Frequently occurring words in negative feedback: "
                f"{terms}. These are recurring terms, not automatically "
                "confirmed causes of dissatisfaction."
            )
        else:
            insights.append(
                "Negative feedback is present, but no frequent terms "
                "were identified for the word summary."
            )

    # Most frequent terms in positive feedback
    if summary["positive_count"] > 0:
        positive_words = find_common_words(
            results_df, "Positive", top_n=5
        )

        if positive_words:
            terms = ", ".join(
                f"{word} ({count})"
                for word, count in positive_words
            )
            insights.append(
                "Frequently occurring words in positive feedback: "
                f"{terms}. Review the original comments to understand "
                "what customers or users valued."
            )

    return insights


def generate_recommendations(summary, results_df):
    """Generate practical, industry-neutral recommendations."""

    recommendations = []

    negative_feedback = results_df[
        results_df["Sentiment"] == "Negative"
    ]

    negative_words = find_common_words(
        results_df, "Negative", top_n=100
    )

    negative_terms = {word for word, count in negative_words}

    # Recommend action only when relevant words occur in negative feedback.
    for theme, keywords in ISSUE_THEMES.items():
        matched_terms = negative_terms.intersection(keywords)

        if matched_terms:
            recommendations.append({
                "priority": (
                    "High"
                    if summary["negative_percentage"] >= 30
                    else "Medium"
                ),
                "area": theme.title(),
                "evidence": (
                    f"Terms found in negative feedback: "
                    f"{', '.join(sorted(matched_terms))}."
                ),
                "action": THEME_RECOMMENDATIONS[theme],
            })

    # Positive feedback can help identify strengths to preserve.
    positive_words = find_common_words(
        results_df, "Positive", top_n=100
    )
    positive_terms = {word for word, count in positive_words}

    strength_terms = positive_terms.intersection({
        "helpful", "excellent", "friendly", "reliable", "easy",
        "clear", "efficient", "useful", "professional", "fast",
        "quality", "responsive",
    })

    if strength_terms:
        recommendations.append({
            "priority": "Maintain",
            "area": "Existing strengths",
            "evidence": (
                "Positive feedback includes: "
                f"{', '.join(sorted(strength_terms))}."
            ),
            "action": (
                "Review the original positive comments to understand "
                "what users value. Preserve those strengths and monitor "
                "future feedback to see whether they remain consistent."
            ),
        })

    # Avoid claiming a specific issue when the evidence is insufficient.
    if not recommendations:
        recommendations.append({
            "priority": "Monitor",
            "area": "Further review",
            "evidence": (
                f"{len(negative_feedback):,} negative responses were "
                "available, but the current keyword rules did not identify "
                "a specific issue theme."
            ),
            "action": (
                "Review a sample of the original feedback manually, "
                "identify recurring concerns, and expand the theme rules "
                "when a consistent pattern is supported by the data."
            ),
        })

    return recommendations


def create_report_data(summary, results_df):
    """Collect report metrics, word summaries, and recommendations."""

    return {
        "total_feedback": summary["total_reviews"],
        "positive_count": summary["positive_count"],
        "negative_count": summary["negative_count"],
        "neutral_count": summary["neutral_count"],
        "positive_percentage": summary["positive_percentage"],
        "negative_percentage": summary["negative_percentage"],
        "neutral_percentage": summary["neutral_percentage"],
        "positive_words": find_common_words(
            results_df, "Positive", top_n=5
        ),
        "negative_words": find_common_words(
            results_df, "Negative", top_n=5
        ),
        "neutral_words": find_common_words(
            results_df, "Neutral", top_n=5
        ),
        "insights": generate_report_insights(summary, results_df),
        "recommendations": generate_recommendations(summary, results_df),
    }
