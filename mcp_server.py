from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from web_operations import serp_search, reddit_search_api, reddit_post_retrieval
from llm_prompt import (
    get_google_analysis_messages,
    get_bing_analysis_messages,
    get_reddit_analysis_messages,
    get_synthesis_messages,
)
from langchain_openai import ChatOpenAI

app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini")  # Use your LLM

# -------------------------------
# Request models
# -------------------------------
class SearchRequest(BaseModel):
    query: str

class RedditPostsRequest(BaseModel):
    urls: List[str]

class AnalysisRequest(BaseModel):
    user_question: str
    google_results: Dict[str, Any]
    bing_results: Dict[str, Any]
    reddit_results: Dict[str, Any]
    reddit_post_data: List[Dict[str, Any]]

# -------------------------------
# Endpoints
# -------------------------------
@app.post("/search")
async def search(req: SearchRequest):
    try:
        google = serp_search(req.query, "google")
        bing = serp_search(req.query, "bing")
        reddit = reddit_search_api(req.query)
        return {"google": google, "bing": bing, "reddit": reddit}
    except Exception as e:
        return {"error": str(e)}

@app.post("/reddit_posts")
async def reddit_posts(req: RedditPostsRequest):
    try:
        posts = reddit_post_retrieval(req.urls)
        return {"posts": posts}
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze")
async def analyze(req: AnalysisRequest):
    try:
        # 1️⃣ Google analysis
        google_msgs = get_google_analysis_messages(req.user_question, req.google_results)
        google_analysis = llm.invoke(google_msgs).content

        # 2️⃣ Bing analysis
        bing_msgs = get_bing_analysis_messages(req.user_question, req.bing_results)
        bing_analysis = llm.invoke(bing_msgs).content

        # 3️⃣ Reddit analysis
        reddit_msgs = get_reddit_analysis_messages(
            req.user_question, req.reddit_results, req.reddit_post_data
        )
        reddit_analysis = llm.invoke(reddit_msgs).content

        # 4️⃣ Final synthesis
        synthesis_msgs = get_synthesis_messages(
            req.user_question, google_analysis, bing_analysis, reddit_analysis
        )
        final_answer = llm.invoke(synthesis_msgs).content

        return {
            "google_analysis": google_analysis,
            "bing_analysis": bing_analysis,
            "reddit_analysis": reddit_analysis,
            "final_answer": final_answer,
        }
    except Exception as e:
        return {"error": str(e)}
