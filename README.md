# 🔎 OmniSearch_Agent

**OmniSearch_Agent** is your all-in-one **AI research assistant**!  
It gathers information from **Google, Bing, and Reddit**, analyzes it using AI, and synthesizes a **comprehensive final answer**.  

✨ **Multi-source, multi-perspective, all in one!**  

---

## 🌟 Features

- 🌐 **Multi-Source Research:** Google, Bing & Reddit in parallel  
- 🤖 **LLM Analysis:** GPT-4o-mini analyzes & summarizes results  
- 📝 **Reddit Insights:** Extracts most valuable posts & comments  
- 🔗 **Final Answer Synthesis:** Combines all insights into one answer  
- 💻 **Streamlit Web App:** Interactive & user-friendly  
- ⚡ **CLI & API Ready:** Use in terminal or via FastAPI  
- 🛡 **MCP Server:** Handles multi-step processing and parallel computation  
- 🛠 **BrightData Integration:** Efficient SERP & Reddit scraping  

---

### 🌐 Streamlit Demo (app.py)  

![Streamlit Demo](ezgif.com-speed%20(9).gif)
## 💻 Dependencies

- Python 3.10+
- streamlit            # For the interactive web app
- fastapi              # For MCP server
- uvicorn              # For running the FastAPI MCP server
- requests             # For API calls & web scraping
- pydantic             # Data validation for MCP requests
- langgraph            # Workflow graph for multi-step processing
- langchain_openai     # LLM integration
- python-dotenv        # Load environment variables (.env)


## 📂 Project Structure

```
OMNISEARCHAGENT/
├─ app.py # 🌐 Streamlit frontend
├─ main.py # 💻 CLI workflow
├─ mcp_server.py # ⚡ FastAPI backend
├─ llm_prompt.py # 📝 LLM prompt templates
├─ web_operations.py # 🔎 Web & Reddit data retrieval
├─ snapshot_operations.py # 📥 BrightData snapshot handling
├─ .env # 🔑 API keys
└─ 📖 README.md
```
## 🚀 Quick Start

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/OmniSearch_Agent.git
cd OmniSearch_Agent
```
2. **Install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
3. **Setup .env**

```bash
OPENAI_API_KEY=your_openai_api_key
BRIGHTDATA_API_KEY=your_brightdata_api_key
```
 **🌐 Streamlit App**

```bash
streamlit run app.py
```
- Type your question 📝
- Click **Search 🚀**
- View **Google, Bing, Reddit analyses & Final Answer**

**💻 CLI Chatbot**

```bash
python main.py
```
- Type a question 📝
- Receive multi-source analysis and final answer
- Type `exit` to quit

### 💻 CLI Demo (main.py)  

![CLI Demo](ezgif.com-speed%20(8).gif)

**⚡ MCP FastAPI Server**

```bash
uvicorn mcp_server:app --reload
```
### ⚡ MCP FastAPI Server

The MCP (Model Context Protocol) server manages **context-aware multi-source processing**. It exposes endpoints to handle the full AI workflow:

- **/search** `POST` → Searches **Google, Bing, and Reddit** for a user query.
- **/reddit_posts** `POST` → Retrieves detailed Reddit posts for selected URLs.
- **/analyze** `POST` → Analyzes all source results with LLM and synthesizes a **final comprehensive answer**.

> 💡 MCP ensures the **user question context is preserved across all steps**, producing consistent and coherent answers.

## 🛡 License

MIT License






