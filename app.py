
import streamlit as st

import pandas as pd
from io import BytesIO
from docx import Document

from analysis import analyze_feedback, calculate_summary

from visualizations import (
    create_sentiment_chart,
    create_sentiment_donut,
    create_sentiment_comparison,
    create_score_distribution,
)

from insights import generate_insights
from report_analysis import (
    generate_report_insights,
    generate_recommendations,
    create_report_data,
    find_common_words,
)
from theme import THEMES


def load_feedback_file(uploaded_file):
    """Read supported file formats into a Pandas DataFrame."""

    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    elif filename.endswith(".txt"):
        text = uploaded_file.getvalue().decode("utf-8-sig")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return pd.DataFrame({"feedback": lines})

    elif filename.endswith(".docx"):
        document = Document(BytesIO(uploaded_file.getvalue()))
        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]
        return pd.DataFrame({"feedback": paragraphs})

    else:
        raise ValueError("This file format is not supported.")
 
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FeedbackLens AI | Sentiment Insights",
    page_icon="🌸",
    layout="wide",
)


# --------------------------------------------------
# THEME SELECTION
# --------------------------------------------------

st.sidebar.image("logo.png", width=150)

st.sidebar.markdown(
    """
    <p style="font-size: 13px; opacity: 0.75;">
        A softer way to understand feedback
    </p>
    """,
    unsafe_allow_html=True,
)

theme_name = st.sidebar.selectbox(
    "Choose your aesthetic",
    ["Standard Streamlit"] + list(THEMES.keys()),
)

theme = (
    None
    if theme_name == "Standard Streamlit"
    else THEMES[theme_name]
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.markdown(
    """
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #FBF7FC 0%,
            #F4EDF9 100%
        );
        border-right: 1px solid #E2D5EC;
    }

    /* Sidebar padding */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    /* Navigation heading */
    [data-testid="stSidebar"] h3 {
        color: #655078;
        font-size: 18px;
        font-weight: 700;
        padding: 10px 12px;
        margin-bottom: 12px;
    }

    /* Navigation labels */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #756580;
        font-size: 14px;
        font-weight: 500;
    }

    /* Navigation options container */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 8px;
    }

    /* Individual navigation options */
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
        border-radius: 12px;
    }

    /* Divider styling */
    [data-testid="stSidebar"] hr {
        border-color: #E3D6EC;
        margin: 18px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.divider()

st.sidebar.markdown("### Explore FeedbackLens")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Sentiment Analysis",
        "Insights & Recommendations",
        "Feedback Explorer",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()


# --------------------------------------------------
# CUSTOM UI STYLING
# --------------------------------------------------

if theme is not None:
    st.markdown(
        f"""
        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
        );

        .stApp {{
            background: {theme["background"]};
            font-family: 'DM Sans', sans-serif;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        [data-testid="stSidebar"] {{
            background: {theme["sidebar"]};
            border-right: 1px solid {theme["accent"]}44;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {{
            color: {theme["text"]};
        }}

        .block-container {{
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}

        h1, h2, h3 {{
            color: {theme["text"]} !important;
            font-family: 'Playfair Display', serif !important;
        }}

        .stApp p,
        .stApp label {{
            color: {theme["text"]};
        }}

        [data-testid="stMetric"] {{
            background: {theme["card"]};
            border: 1px solid {theme["accent"]}55;
            border-radius: 18px;
            padding: 20px 22px;
            box-shadow: 0 5px 18px rgba(70, 50, 70, 0.05);
        }}

        [data-testid="stMetricLabel"] p {{
            font-size: 0.9rem;
            font-weight: 600;
        }}

        [data-testid="stMetricValue"] {{
            font-weight: 700;
        }}

        .stButton > button,
        .stDownloadButton > button {{
            background: {theme["accent"]};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.55rem 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            filter: brightness(0.96);
            transform: translateY(-1px);
        }}

        [data-testid="stFileUploader"] {{
            background: {theme["card"]};
            border: 1px dashed {theme["accent"]};
            border-radius: 16px;
            padding: 12px;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid {theme["accent"]}55;
            border-radius: 14px;
            overflow: hidden;
        }}

        hr {{
            border-color: {theme["accent"]}44;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )



# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <style>
    .feedbacklens-header {
        background-color: #F7F0FA;
        padding: 28px;
        border-radius: 22px;
        text-align: center;
        border: 1px solid #E9DDF0;
    }

    .feedbacklens-header p {
        color: #75677D;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="feedbacklens-header">
        <p>✦ AI-POWERED FEEDBACK ANALYSIS</p>
        <h1>FeedbackLens AI </h1>
        <p>
            Every opinion holds insight. Discover the patterns, understand the sentiment, and turn feedback into action.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()



# --------------------------------------------------
# DATA UPLOAD
# --------------------------------------------------

st.subheader("Let's explore your feedback")

st.write(
    "Upload a CSV file containing a column named `feedback` "
    "to begin your analysis."
)


uploaded_file = st.file_uploader(
    "Upload your feedback",
    type=["csv", "xlsx", "xls", "txt", "docx"],
    help=(
        "Supported formats: CSV, Excel, TXT, and Word DOCX. "
        "CSV and Excel files must contain a 'feedback' column."
    ),
)



# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

try:
    results_df = analyze_feedback(uploaded_file)
    summary = calculate_summary(results_df)

except Exception as error:
    st.error(f"Unable to analyze the feedback: {error}")
    st.stop()


report_data = create_report_data(summary, results_df)


# --------------------------------------------------
# OVERVIEW METRICS
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Soft sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FBF7FC 0%, #F4EDF9 100%);
        border-right: 1px solid #E5D9ED;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    /* Rounded metric cards */
    [data-testid="stMetric"] {
        background: #FFFCFF;
        border: 1px solid #E5D8EF;
        border-radius: 16px;
        padding: 20px 18px;
        box-shadow: 0 3px 12px rgba(117, 86, 143, 0.06);
        transition: all 0.2s ease;
    }

    /* Gentle hover effect */
    [data-testid="stMetric"]:hover {
        border-color: #C9B0DD;
        box-shadow: 0 5px 16px rgba(117, 86, 143, 0.12);
        transform: translateY(-2px);
    }

    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #756580;
        font-size: 14px;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #655078;
        font-weight: 700;
    }


    /* Navigation heading */
    [data-testid="stSidebar"] h3 {
        color: #655078;
        font-size: 18px;
        font-weight: 700;
        padding: 10px 12px;
        margin-bottom: 12px;
    }

    /* Space between navigation items */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 10px;
    }

    /* Boxed navigation items */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: #FFFCFF;
        border: 1px solid #E5D8EF;
        border-radius: 13px;
        padding: 13px 14px;
        color: #756580;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* Hover effect */
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #F0E5F7;
        border-color: #C9B0DD;
        color: #5E4675;
    }

    /* Divider */
    [data-testid="stSidebar"] hr {
        border-color: #E5D9ED;
        margin: 18px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if page == "Overview":

    st.markdown("## Your feedback at a glance")
    st.write(
        "A little snapshot of the feelings behind your feedback."
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            label="Total feedback",
            value=summary["total_reviews"],
            help="Total number of feedback entries analyzed.",
        )

    with metric2:
        st.metric(
            label="Positive",
            value=f'{summary["positive_percentage"]:.1f}%',
            help="Percentage classified as positive.",
        )

    with metric3:
        st.metric(
            label="Negative",
            value=f'{summary["negative_percentage"]:.1f}%',
            help="Percentage classified as negative.",
        )

    with metric4:
        st.metric(
            label="Neutral",
            value=f'{summary["neutral_percentage"]:.1f}%',
            help="Percentage classified as neutral.",
        )

# --------------------------------------------------
# SENTIMENT CHART
# --------------------------------------------------



if page == "Sentiment Analysis":

    st.markdown("## Sentiment Studio")
    st.write(
        "Explore the emotions behind your feedback through "
        "multiple visual perspectives."
    )

    st.divider()

    # SENTIMENT SUMMARY CARDS
    st.markdown("### Your sentiment snapshot")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Positive feedback",
            f'{summary["positive_percentage"]:.1f}%',
            f'{summary["positive_count"]} responses',
        )

    with metric2:
        st.metric(
            "Neutral feedback",
            f'{summary["neutral_percentage"]:.1f}%',
            f'{summary["neutral_count"]} responses',
        )

    with metric3:
        st.metric(
            "Negative feedback",
            f'{summary["negative_percentage"]:.1f}%',
            f'{summary["negative_count"]} responses',
        )

    st.divider()

    # DONUT CHART AND COMPARISON CHART
    st.markdown("### Sentiment breakdown")

    chart_left, chart_right = st.columns(2, gap="large")

    with chart_left:
        st.pyplot(
            create_sentiment_donut(results_df, theme),
            use_container_width=True,
        )

    with chart_right:
        st.pyplot(
            create_sentiment_comparison(results_df, theme),
            use_container_width=True,
        )

    st.divider()

    # COMPOUND SCORE DISTRIBUTION
    st.markdown("### Sentiment score distribution")

    st.write(
        "See how strongly the feedback leans positive or negative. "
        "Scores closer to zero indicate more neutral sentiment."
    )

    st.pyplot(
        create_score_distribution(results_df),
        use_container_width=True,
    )

    st.caption(
        "FeedbackLens AI uses VADER compound sentiment scores, "
        "which range from -1 (most negative) to +1 (most positive)."
    )



# --------------------------------------------------
# INSIGHTS & RECOMMENDATIONS PAGE
# --------------------------------------------------

import html
import pandas as pd

if page == "Insights & Recommendations":

    # ---------- PAGE STYLING ----------
    st.markdown("""
        <style>
        .insight-card {
            padding: 18px 20px;
            border-radius: 18px;
            margin: 8px 0 14px 0;
            line-height: 1.65;
            font-size: 14px;
            box-shadow: 0 4px 14px rgba(101, 80, 120, 0.05);
        }

        .lavender {
            background: #F1EAF9;
            border: 1px solid #DCCBEF;
            color: #59466F;
        }

        .blush {
            background: #FCEBF1;
            border: 1px solid #F0CBD9;
            color: #814E63;
        }

        .cream {
            background: #FFFDF7;
            border: 1px solid #EAE0D1;
            color: #685A68;
        }

        .butter {
            background: #FFF5D9;
            border: 1px solid #F0DDA0;
            color: #79612E;
        }

        .insight-number {
            font-size: 28px;
            font-weight: 750;
            margin: 7px 0;
        }

        .insight-label {
            font-size: 13px;
            font-weight: 600;
        }

        .insight-muted {
            font-size: 13px;
            color: #85758F;
            margin-bottom: 15px;
        }

        .word-pill {
            display: inline-block;
            background: #F1EAF9;
            color: #655078;
            border: 1px solid #DCCBEF;
            border-radius: 24px;
            padding: 6px 12px;
            margin: 4px 3px 4px 0;
            font-size: 12px;
        }

        .recommendation-card {
            background: #FFFDFB;
            border: 1px solid #E5D8EF;
            border-radius: 18px;
            padding: 20px;
            margin: 10px 0 16px 0;
            box-shadow: 0 4px 14px rgba(101, 80, 120, 0.05);
        }

        .recommendation-area {
            color: #655078;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .recommendation-label {
            color: #8B7A96;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- QUICK INSIGHTS ----------
    st.divider()
    st.markdown("## Little insights, meaningful changes")
    st.write(
        "A quick interpretation of the overall sentiment results."
    )

    insights = generate_insights(summary)

    insight_colours = ["lavender", "blush", "butter", "cream"]

    if insights:
        for index, insight in enumerate(insights):
            colour = insight_colours[index % len(insight_colours)]

            st.markdown(
                f"""
                <div class="insight-card {colour}">
                    <div class="insight-label">QUICK INSIGHT</div>
                    {html.escape(str(insight))}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info(
            "No specific insights were triggered by the current rules. "
            "Review the sentiment distribution for patterns."
        )

    # ---------- DATA INSIGHTS REPORT ----------
    st.divider()
    st.markdown("## Your feedback story")
    st.write(
        "A closer look at sentiment patterns and descriptive words "
        "found in your feedback."
    )

    # Sentiment summary bubbles
    st.markdown("### Sentiment at a glance")

    sentiment_columns = st.columns(3)

    sentiment_cards = [
        (
            "Positive",
            summary["positive_count"],
            summary["positive_percentage"],
            "lavender",
        ),
        (
            "Negative",
            summary["negative_count"],
            summary["negative_percentage"],
            "blush",
        ),
        (
            "Neutral",
            summary["neutral_count"],
            summary["neutral_percentage"],
            "butter",
        ),
    ]

    for column, (label, count, percentage, colour) in zip(
        sentiment_columns, sentiment_cards
    ):
        with column:
            st.markdown(
                f"""
                <div class="insight-card {colour}">
                    <div class="insight-label">
                        {label} sentiment
                    </div>
                    <div class="insight-number">
                        {percentage:.1f}%
                    </div>
                    <div>{count:,} responses</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Report insights as colourful cards
    report_insights = generate_report_insights(
        summary,
        results_df,
    )

    st.markdown("### What stands out")

    if report_insights:
        for index, insight in enumerate(report_insights):
            colour = insight_colours[index % len(insight_colours)]

            st.markdown(
                f"""
                <div class="insight-card {colour}">
                    {html.escape(str(insight))}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No additional report insights are available.")

    # Word-frequency tables
    st.markdown("### Words behind the feedback")
    st.markdown(
        '<div class="insight-muted">'
        'Explore frequently occurring words in positive and negative '
        'comments. Word frequency alone does not confirm the reason '
        'behind someone’s sentiment.'
        '</div>',
        unsafe_allow_html=True,
    )

    positive_words = find_common_words(
        results_df,
        sentiment="Positive",
        top_n=10,
    )

    negative_words = find_common_words(
        results_df,
        sentiment="Negative",
        top_n=10,
    )

    positive_col, negative_col = st.columns(2, gap="large")

    with positive_col:
        st.markdown("#### Positive feedback")

        if positive_words:
            positive_df = pd.DataFrame(
                positive_words,
                columns=["Word", "Mentions"],
            )

            st.dataframe(
                positive_df,
                hide_index=True,
                width="stretch",
            )

            pills = "".join(
                f'<span class="word-pill">'
                f'{html.escape(str(word))} · {count}'
                f'</span>'
                for word, count in positive_words[:5]
            )

            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No frequent words found in positive feedback.")

    with negative_col:
        st.markdown("#### Negative feedback")

        if negative_words:
            negative_df = pd.DataFrame(
                negative_words,
                columns=["Word", "Mentions"],
            )

            st.dataframe(
                negative_df,
                hide_index=True,
                width="stretch",
            )

            pills = "".join(
                f'<span class="word-pill">'
                f'{html.escape(str(word))} · {count}'
                f'</span>'
                for word, count in negative_words[:5]
            )

            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No frequent words found in negative feedback.")

    st.caption(
        "Mentions count word occurrences, not unique people or comments. "
        "Always review the original feedback before drawing conclusions."
    )

    # ---------- RECOMMENDATIONS ----------
    st.divider()
    st.markdown("## Ideas for improvement")
    st.write(
        "Suggestions based on the sentiment patterns and "
        "descriptive terms identified in your data."
    )

    recommendations = generate_recommendations(
        summary,
        results_df,
    )

    priority_colours = {
        "High": "blush",
        "Medium": "butter",
        "Maintain": "lavender",
        "Monitor": "cream",
    }

    if recommendations:
        for recommendation in recommendations:
            area = html.escape(str(recommendation["area"]))
            priority = html.escape(str(recommendation["priority"]))
            evidence = html.escape(str(recommendation["evidence"]))
            action = html.escape(str(recommendation["action"]))

            colour = priority_colours.get(
                recommendation["priority"],
                "cream",
            )

            st.markdown(
                f"""
                <div class="recommendation-card">
                    <div class="recommendation-area">{area}</div>
                    <div class="insight-card {colour}">
                        <span class="recommendation-label">
                            Priority
                        </span>
                        <br>{priority}
                    </div>
                    <div class="recommendation-label">
                        What the feedback shows
                    </div>
                    <p>{evidence}</p>
                    <div class="recommendation-label">
                        Suggested action
                    </div>
                    <p>{action}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info(
            "There are no recommendations available for this dataset."
        )

# --------------------------------------------------
# FEEDBACK EXPLORER PAGE
# --------------------------------------------------

if page == "Feedback Explorer":

    st.divider()
    st.markdown("## Every response, understood")

    st.write(
        "Review the original feedback alongside its sentiment "
        "classification and compound sentiment score."
    )

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True,
    )

    # DOWNLOAD RESULTS
    st.divider()
    st.markdown("### Export your analysis")

    csv_data = results_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download analyzed feedback",
        data=csv_data,
        file_name="feedback_analysis.csv",
        mime="text/csv",
        use_container_width=False,
    )


# --------------------------------------------------
# FOOTER - SHARED ACROSS ALL PAGES
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 20px 0 10px;
        opacity: 0.75;
        font-size: 13px;
    ">
        <div style="font-size: 22px; margin-bottom: 8px;">🌷</div>
        <strong>FeedbackLens AI</strong>
        <p style="margin: 5px 0;">
            Turning feedback into clearer insights and better decisions.
        </p>
        <p style="font-size: 11px;">
            Built with Python, Streamlit, Pandas, VADER and Matplotlib.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
