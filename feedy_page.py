
import streamlit as st

from feedy import get_feedy_response


def render_feedy_page(results_df, summary):
    """Render the Feedy AI assistant page."""

    st.markdown(
        """
        <div style="padding: 10px 0 20px;">
            <h2 style="color: #9B86B0;">Ask Feedy</h2>
            <p style="color: #8A7B94;">
                Your AI assistant for understanding feedback
                and discovering practical improvements.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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

        with st.chat_message("user"):
            st.markdown(pending_question)

        with st.chat_message("assistant"):
            with st.spinner("Feedy is thinking..."):
                answer = get_feedy_response(
                    pending_question,
                    results_df,
                    summary,
                )
                st.markdown(answer)

        st.session_state.feedy_messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

    if st.button("Clear conversation", key="clear_feedy_chat"):
        st.session_state.feedy_messages = []
        st.rerun()
