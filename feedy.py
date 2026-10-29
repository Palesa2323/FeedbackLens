
import streamlit as st
from google import genai


def get_feedy_response(question, results_df, summary):
    """Generate an AI response based on the analysed feedback."""

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return (
            "My Gemini API key hasn't been configured yet. "
            "Please add GEMINI_API_KEY to your Streamlit secrets."
        )

    if results_df is None or results_df.empty:
        return "Please upload and analyse feedback before asking me questions."

    try:
        client = genai.Client(api_key=api_key)

        # Send a limited sample of feedback, rather than the entire dataset.
        feedback_sample = results_df[
            ["Feedback", "Sentiment", "Score"]
        ].head(100).to_string(index=False)

        prompt = f"""
You are Feedy, the friendly AI feedback assistant inside FeedbackLens AI.

Your job is to help organisations understand feedback and improve their
products, services, communication, and customer experience.

Rules:
- Answer using the supplied feedback and summary.
- Give practical, specific recommendations.
- Clearly distinguish findings from suggestions.
- Never invent statistics or claim that a pattern exists without evidence.
- If the data doesn't answer a question, say so.
- Be professional, warm, concise, and easy to understand.
- Protect privacy. Do not attempt to identify people.

FEEDBACK SUMMARY:
{summary}

SAMPLE OF ANALYSED FEEDBACK:
{feedback_sample}

USER QUESTION:
{question}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text or "I couldn't generate a response. Please try again."

    except Exception:
        return (
            "I couldn't connect to the AI service just now. "
            "Please check your API key and connection, then try again."
        )
