import streamlit as st
import requests

MCP_URL = "http://localhost:8000"  # MCP server

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="🔎 Multi-Source Research Agent",
    page_icon="🔎",
    layout="wide"
)

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown("""
<style>
    /* Center title */
    .title-center {
        text-align: center;
        font-size: 2rem !important;
        font-weight: bold;
        color: #2E86C1;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #1F618D;
    }

    /* Final Answer highlight: black background */
    .final-answer {
        background-color: #000000;  /* Black background */
        color: #FDFEFE;             /* White text */
        border-left: 5px solid #F7DC6F;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        white-space: pre-wrap;      /* preserves newlines */
    }

    /* Columns text styling */
    .analysis-text {
        white-space: pre-wrap;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown('<p class="title-center">🔎 Multi-Source Research Agent</p>', unsafe_allow_html=True)

# -------------------------------
# User Input
# -------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("💡 Ask me anything:", placeholder="e.g. What are the latest AI trends?")
with col2:
    submit = st.button("🚀 Search")

# -------------------------------
# Handle Submission
# -------------------------------
if submit and user_input:
    with st.spinner("⏳ Gathering insights from Google, Bing & Reddit..."):
        try:
            # 1️⃣ Call /search on MCP
            search_resp = requests.post(
                f"{MCP_URL}/search",
                json={"query": user_input}
            ).json()

            # 2️⃣ Reddit Posts retrieval
            reddit_posts = []
            if "reddit" in search_resp and "parsed_posts" in search_resp["reddit"]:
                reddit_posts = requests.post(
                    f"{MCP_URL}/reddit_posts",
                    json={"urls": search_resp["reddit"]["parsed_posts"]}
                ).json().get("posts", [])

            # 3️⃣ Call /analyze
            analysis_resp = requests.post(
                f"{MCP_URL}/analyze",
                json={
                    "user_question": user_input,
                    "google_results": search_resp.get("google", {}),
                    "bing_results": search_resp.get("bing", {}),
                    "reddit_results": search_resp.get("reddit", {}),
                    "reddit_post_data": reddit_posts,
                }
            ).json()

            # -------------------------------
            # Display Final Answer
            # -------------------------------
            st.markdown("### 📌 Final Answer")
            st.markdown(
                f"<div class='final-answer'>{analysis_resp.get('final_answer', 'No answer generated.')}</div>",
                unsafe_allow_html=True
            )

            # -------------------------------
            # Two-column layout for analysis
            # -------------------------------
            col_g, col_b = st.columns(2)

            with col_g:
                with st.expander("🔍 Google Analysis"):
                    st.markdown(
                        f"<div class='analysis-text'>{analysis_resp.get('google_analysis', 'N/A')}</div>",
                        unsafe_allow_html=True
                    )

                with st.expander("🟦 Bing Analysis"):
                    st.markdown(
                        f"<div class='analysis-text'>{analysis_resp.get('bing_analysis', 'N/A')}</div>",
                        unsafe_allow_html=True
                    )

            with col_b:
                with st.expander("👥 Reddit Analysis"):
                    st.markdown(
                        f"<div class='analysis-text'>{analysis_resp.get('reddit_analysis', 'N/A')}</div>",
                        unsafe_allow_html=True
                    )

        except Exception as e:
            st.error(f"❌ Error: {e}")

