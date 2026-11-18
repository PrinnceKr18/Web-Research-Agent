# Web Research Agent

An AI-assisted web research toolkit built with Python, LangChain, Groq, Tavily, and the Playwright MCP server. It can search the web, browse and extract webpage content, summarize research findings, and demonstrate tool-calling and structured output with LangChain agents.

## Features

- Search the web with the Tavily API
- Extract content from multiple websites with Playwright MCP
- Generate AI research summaries with Groq-hosted models
- Run an autonomous browser research agent
- Demonstrate LangChain memory, middleware, tool calling, and structured responses
- Normalize and remove duplicate URLs from search results
- Save multi-source research output to JSON

## Project Files

| File | Purpose |
| --- | --- |
| `main.py` | Interactive travel assistant with weather and population tools |
| `tavily_search.py` | Standalone Tavily web search |
| `browser_agent.py` | Browser navigation, page extraction, and Groq summary |
| `autonomous_browser_agent.py` | Autonomous LangChain agent with Playwright browser tools |
| `multi_source_research.py` | Search, visit multiple sites, and save research results |
| `structured_output.py` | City report generated with a Pydantic response schema |
| `tools.py` | Example weather and population LangChain tools |
| `middleware.py` | Tool-call logging middleware |
| `url_manager.py` | URL validation, normalization, and deduplication |
| `test_groq.py` | Quick Groq model and tool-call test |
| `test_browser.py` | List tools exposed by the Playwright MCP server |

## Requirements

- Python 3.10 or newer
- Node.js and npm (for Playwright MCP)
- Groq API key
- Tavily API key

## Installation

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/PrinnceKr18/Web-Research-Agent.git
cd Web-Research-Agent
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

Run a standalone Tavily search:

```powershell
python tavily_search.py
```

Run the interactive travel assistant:

```powershell
python main.py
```

Extract and summarize a webpage:

```powershell
python browser_agent.py
```

Run the autonomous browser research agent:

```powershell
python autonomous_browser_agent.py
```

Search and research up to three unique websites:

```powershell
python multi_source_research.py
```

Generate a city report with structured output:

```powershell
python structured_output.py
```

The Playwright MCP server is started automatically through `npx` by scripts that use browser tools. Node.js and npm must be available in `PATH`.

## Testing

Check Groq connectivity and tool binding:

```powershell
python test_groq.py
```

Check the Playwright MCP tools:

```powershell
python test_browser.py
```

## Output

`multi_source_research.py` writes the collected sources and extracted content to `research_results.json`.

