import streamlit as st

from rag import answer_question

st.set_page_config(
    page_title="CyberSec RAG Assistant",
    layout="wide"
)

st.title(
    "🛡️ CyberSec RAG Assistant"
)

question = st.text_input(
    "Ask a Cyber Security Question"
)

if st.button("Ask"):

    if question:

        with st.spinner(
            "Searching..."
        ):

            response = answer_question(
                question
            )

            st.subheader(
                "Answer"
            )

            st.write(
                response.answer
            )

            st.subheader(
                "Sources"
            )

            for source in response.sources:

                st.markdown(
                    f"""
**File:** {source.filename}

**Page:** {source.page}
"""
                )