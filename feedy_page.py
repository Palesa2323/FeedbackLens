
import streamlit as st

from feedy import get_feedy_response
import html
import re


def render_chat_bubble(role, content):
    """Display themed chat bubbles with Markdown formatting."""
    is_user = role == "user"
    bubble_class = "user-bubble" if is_user else "ai-bubble"
    alignment = "flex-end" if is_user else "flex-start"
    label = "You" if is_user else "Feedy ✦"

    # Escape HTML first to keep message content safe.
    safe_content = html.escape(str(content))

    # Convert common Markdown formatting to HTML.
    safe_content = re.sub(
        r"^#### (.+)$", r"<h4>\1</h4>", safe_content, flags=re.MULTILINE
    )
    safe_content = re.sub(
        r"^### (.+)$", r"<h3>\1</h3>", safe_content, flags=re.MULTILINE
    )
    safe_content = re.sub(
        r"^## (.+)$", r"<h2>\1</h2>", safe_content, flags=re.MULTILINE
    )
    safe_content = re.sub(
        r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe_content
    )
    safe_content = re.sub(
        r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", safe_content
    )

    # Convert bullet points.
    safe_content = re.sub(
        r"(?m)^[*-] (.+)$", r"• \1", safe_content
    )

    # Preserve line breaks.
    safe_content = safe_content.replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="chat-row" style="justify-content: {alignment};">
            <div class="chat-bubble {bubble_class}">
                <div class="bubble-label">{label}</div>
                <div class="bubble-content">{safe_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_feedy_page(results_df, summary):
    """Render the Feedy AI assistant page."""


    st.markdown("""
    <style>
    .chat-row {
        display: flex;
        width: 100%;
        margin: 14px 0;
    }

    .chat-bubble {
        max-width: 78%;
        padding: 13px 17px;
        border-radius: 20px;
        overflow-wrap: anywhere;
        font-size: 15px;
        line-height: 1.65;
        box-shadow: 0 4px 14px rgba(91, 67, 120, 0.07);
    }

    .user-bubble {
        background: linear-gradient(135deg, #e7d9ff, #f6dce9);
        color: #40334f;
        border-bottom-right-radius: 6px;
    }

    .ai-bubble {
        background: #fffaf5;
        color: #453a50;
        border: 1px solid #eadff2;
        border-bottom-left-radius: 6px;
    }

    .bubble-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
        color: #9275ac;
    }

    .bubble-content {
        overflow-wrap: anywhere;
    }

    </style>
    """, unsafe_allow_html=True)


    if results_df is None or results_df.empty:
        st.info("Upload and analyse feedback first, then come back to chat with Feedy.")
        return

    if "feedy_messages" not in st.session_state:
        st.session_state.feedy_messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I'm Feedy, your FeedbackLens AI assistant. 💜\n\n"
                    "I can help you understand feedback, identify recurring "
                    "complaints, and suggest practical improvements. "
                    "What would you like to explore?"
                ),
            }
        ]

    # Suggested questions
    st.markdown("##### Need a starting point?")

    suggestions = [
        "What should we improve first?",
        "What are people unhappy about?",
        "What are people praising?",
    ]

    columns = st.columns(3)

    for index, suggestion in enumerate(suggestions):
        with columns[index]:
            if st.button(suggestion, key=f"feedy_suggestion_{index}", use_container_width=True):
                st.session_state.feedy_pending_question = suggestion

    # Display conversation history
    for message in st.session_state.feedy_messages:
        render_chat_bubble(
            message["role"],
            message["content"]
        )
    question = st.chat_input("Ask Feedy about your feedback...")

    # Handle typed questions and suggested questions
    if question:
        st.session_state.feedy_pending_question = question

    pending_question = st.session_state.pop(
        "feedy_pending_question", None
    )

    if pending_question:
        st.session_state.feedy_messages.append(
            {"role": "user", "content": pending_question}
        )

        render_chat_bubble("user", pending_question)

        with st.spinner("Feedy is thinking..."):
            answer = get_feedy_response(
                pending_question,
                results_df,
                summary,
            )

        render_chat_bubble("assistant", answer)

        st.session_state.feedy_messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

    if st.button("Clear conversation", key="clear_feedy_chat"):
        st.session_state.feedy_messages = []
        st.rerun()
