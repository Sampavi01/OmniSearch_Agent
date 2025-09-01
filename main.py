import streamlit as st
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from typing import Annotated, List

from web_operations import serp_search, reddit_search_api, reddit_post_retrieval
from llm_prompt import (
    get_reddit_analysis_messages,
    get_google_analysis_messages,
    get_bing_analysis_messages,
    get_reddit_url_analysis_messages,
    get_synthesis_messages
)

load_dotenv()

# ------------------------
# LLM Initialization
# ------------------------
llm = ChatOpenAI(model="gpt-4o-mini")  # Mini model for cost efficiency

# ------------------------
# State definition
# ------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str | None
    google_results: str | None
    bing_results: str | None
    reddit_results: str | None
    selected_reddit_urls: list[str] | None
    reddit_post_data: list | None
    google_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    final_answer: str | None

class RedditURLAnalysis(BaseModel):
    selected_urls: List[str] = Field(
        description="List of Reddit URLs that contain valuable information for answering the user's question"
    )

# ------------------------
# Node functions (same as CLI version)
# ------------------------
def google_search(state: State):
    user_question = state.get("user_question", "")
    google_results = serp_search(user_question, engine="google")
    return {"google_results": google_results}

def bing_search(state: State):
    user_question = state.get("user_question", "")
    bing_results = serp_search(user_question, engine="bing")
    return {"bing_results": bing_results}

def reddit_search(state: State):
    user_question = state.get("user_question", "")
    reddit_results = reddit_search_api(keyword=user_question)
    return {"reddit_results": reddit_results}

def analyze_reddit_posts(state: State):
    reddit_results = state.get("reddit_results", "")
    if not reddit_results:
        return {"selected_reddit_urls": []}

    structured_llm = llm.with_structured_output(RedditURLAnalysis)
    messages = get_reddit_url_analysis_messages(state.get("user_question", ""), reddit_results)

    try:
        analysis = structured_llm.invoke(messages)
        selected_urls = analysis.selected_urls
    except Exception:
        selected_urls = []

    return {"selected_reddit_urls": selected_urls}

def retrieve_reddit_posts(state: State):
    selected_urls = state.get("selected_reddit_urls", [])
    if not selected_urls:
        return {"reddit_post_data": []}
    reddit_post_data = reddit_post_retrieval(selected_urls)
    return {"reddit_post_data": reddit_post_data}

def analyze_google_results(state: State):
    messages = get_google_analysis_messages(state["user_question"], state.get("google_results", ""))
    reply = llm.invoke(messages)
    return {"google_analysis": reply.content}

def analyze_bing_results(state: State):
    messages = get_bing_analysis_messages(state["user_question"], state.get("bing_results", ""))
    reply = llm.invoke(messages)
    return {"bing_analysis": reply.content}

def analyze_reddit_results(state: State):
    messages = get_reddit_analysis_messages(
        state["user_question"],
        state.get("reddit_results", ""),
        state.get("reddit_post_data", "")
    )
    reply = llm.invoke(messages)
    return {"reddit_analysis": reply.content}

def synthesize_analyses(state: State):
    messages = get_synthesis_messages(
        state["user_question"],
        state.get("google_analysis", ""),
        state.get("bing_analysis", ""),
        state.get("reddit_analysis", "")
    )
    reply = llm.invoke(messages)
    final_answer = reply.content
    return {"final_answer": final_answer}

# ------------------------
# Build graph
# ------------------------
graph_builder = StateGraph(State)
graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)
graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
graph_builder.add_node("analyze_google_results", analyze_google_results)
graph_builder.add_node("analyze_bing_results", analyze_bing_results)
graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
graph_builder.add_node("synthesize_analyses", synthesize_analyses)

graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")
graph_builder.add_edge("google_search", "analyze_reddit_posts")
graph_builder.add_edge("bing_search", "analyze_reddit_posts")
graph_builder.add_edge("reddit_search", "analyze_reddit_posts")
graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_google_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_bing_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_reddit_results")
graph_builder.add_edge("analyze_google_results", "synthesize_analyses")
graph_builder.add_edge("analyze_bing_results", "synthesize_analyses")
graph_builder.add_edge("analyze_reddit_results", "synthesize_analyses")
graph_builder.add_edge("synthesize_analyses", END)
graph = graph_builder.compile()

# ------------------------
# Streamlit UI
# ------------------------
st.title("Multi-Source Research Agent")

user_input = st.text_input("Ask me anything:")

if st.button("Submit") and user_input:
    state = {
        "messages": [{"role": "user", "content": user_input}],
        "user_question": user_input,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
    }

    with st.spinner("Running searches and analyzing..."):
        final_state = graph.invoke(state)
        answer = final_state.get("final_answer", "No answer found.")

    st.subheader("Final Answer")
    st.write(answer)
