import streamlit as st

from analysis import analyze_feedback, calculate_summary
from visualizations import create_sentiment_chart
from insights import generate_insights

#configuring the page layout and title
st.set_page_config(
    page_title="FeedbackLens - Sentiment Analysis",
    page_icon=":bar_chart:",
    layout="wide"
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

results_df = analyze_feedback()

summary = calculate_summary(results_df)

st.subheader("Sentiment Overview")
st.metric("Total Feedback", summary["total_reviews"])

fig = create_sentiment_chart(results_df)
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
    
st.subheader("Analyzed Feedback")

st.dataframe(
    results_df,
    use_container_width=True
)