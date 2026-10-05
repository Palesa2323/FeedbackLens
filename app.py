import streamlit as st

from analysis import analyze_feedback, calculate_summary
from visualizations import create_sentiment_chart
from insights import generate_insights
from report_analysis import (
    generate_report_insights,
    generate_recommendations,
    create_report_data
)
from theme import THEMES

#configuring the page layout and title
st.set_page_config(
    page_title="FeedbackLens - Sentiment Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)
# Theme selection
theme_name = st.sidebar.selectbox(
    "Choose a theme",
    ["Standard Streamlit"] + list(THEMES.keys())
)

if theme_name == "Standard Streamlit":
    theme = None
else:
    theme = THEMES[theme_name]

# Applying the selected theme
if theme is not None:
    st.markdown(
        f"""
        <style>

        .stApp {{
            background-color: {theme["background"]};
        }}

        .stApp p,
        .stApp label,
        .stApp span {{
            color: {theme["text"]};
        }}

        [data-testid="stSidebar"] {{
            background-color: {theme["sidebar"]};
        }}

        [data-testid="stMetric"] {{
            background-color: {theme["card"]};
            border-radius: 16px;
            padding: 18px;
            border: 1px solid {theme["accent"]};
        }}

        h1, h2, h3 {{
            color: {theme["text"]} !important;
        }}

        .stButton > button {{
            background-color: {theme["accent"]};
            color: white;
            border: none;
            border-radius: 10px;
        }}

        .stDownloadButton > button {{
            background-color: {theme["accent"]};
            color: white;
            border: none;
            border-radius: 10px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    ) 
# title of the web application
st.title("FeedbackLens - Sentiment Analysis") # st = streamlit
st.subheader("Analyze the sentiment of your feedback data")
st.write(
    "Analyze feedback, identify sentiment patterns, and generate useful insights to improve your services. Upload your feedback data in CSV format and let FeedbackLens do the rest!"
)

uploaded_file = st.file_uploader(
    "Upload your feedback CSV file",
    type=["csv"]
    )

results_df = analyze_feedback(uploaded_file)

summary = calculate_summary(results_df)

report_data = create_report_data(
    summary,
    results_df)   

st.subheader("Sentiment Overview")
st.metric("Total Feedback", summary["total_reviews"])

fig = create_sentiment_chart(results_df, theme)
st.pyplot(fig)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Positive Feedback", f"{summary['positive_percentage']:.1f}%")
with col2:
    st.metric("Negative Feedback", f"{summary['negative_percentage']:.1f}%") 
with col3:
    st.metric("Neutral Feedback", f"{summary['neutral_percentage']:.1f}%")
    
    
st.subheader("Insights")
insights = generate_insights(summary)

for insight in insights:
    st.write(f"- {insight}")
    
st.subheader("Data Insights Report")
report_insights = generate_report_insights(
    summary,
    results_df)

for insight in report_insights:
    st.write("•", insight)

st.subheader("Recommendations")
recommendations = generate_recommendations(summary, results_df)

for recommendation in recommendations:
    st.write("•", recommendation)

st.subheader("Analyzed Feedback")

st.dataframe(
    results_df,
    use_container_width=True
)

csv_data = results_df.to_csv(index=False)

st.download_button(
    label="Download Analyzed Feedback as CSV",
    data=csv_data,
    file_name="feedback_analysis.csv",
    mime="text/csv"
)