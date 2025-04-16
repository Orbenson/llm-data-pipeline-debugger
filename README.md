# 🧠 LLM-Driven Data Pipeline Debugger

An intelligent, modular system that uses **Large Language Models (LLMs)** to automatically analyze pipeline logs, validate datasets, and suggest actionable fixes when errors occur. This project leverages **Google Gemini**, **LangChain**, **LangGraph**, and **Great Expectations**, forming a complete end-to-end debugging assistant for data engineers and ML pipeline developers.

---

## 🔍 Key Features

- **MCP (Memory-Compute-Prompt) Architecture**
  - Memory: Persistent JSON store of historical errors and resolutions
  - Compute: Rule-based validation using Great Expectations
  - Prompt: LLM-driven log summarization and fix suggestions (via Gemini)

- **A2A (Agent-to-Agent Coordination)**  
  Modular `LogAnalysisAgent` and `DataValidationAgent` components communicate via shared memory and orchestrate troubleshooting.

- **LangGraph Integration**
  - Future-proofed for branching and conditional reasoning
  - Enables custom agent workflows for advanced scenarios

- **Flexible LLM Backends**
  - Default: Google Gemini (`gemini-2.0-flash`)
  - OpenAI GPT-compatible fallback if `.env` provides `OPENAI_API_KEY`

- **No OpenAI Key? No Problem!**
  - Gemini runs using the free-tier API and works fully out of the box

---

## 🧱 Project Structure

```
llm-data-pipeline-debugger/
│
├── cli.py                      # Main entrypoint for running the debugger
├── config.yaml                 # Pipeline config (paths, expectations, model)
├── .env.example                # Example env file (use your own secrets)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Containerized build for production
│
├── data/                       # Sample datasets
│   └── sample_dataset.csv
│
├── logs/                       # Sample pipeline logs
│   └── sample_pipeline_error.log
│
├── memory/                     # JSON memory file for past errors
│   └── past_errors.json
│
├── debug_reports/              # Auto-saved analysis summaries and validation output
│
├── pipeline_debugger/
│   ├── orchestrator.py         # Main logic combining agents and output
│   ├── config.py               # YAML loader and environment integration
│   ├── logger.py               # Logging setup
│   ├── memory.py               # MemoryManager class (persistent storage)
│   ├── llm.py                  # LLMChain setup with Gemini/OpenAI
│   └── agents/
│       ├── log_agent.py        # LogAnalysisAgent using LLM
│       └── validation_agent.py # DataValidationAgent using Great Expectations
```

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/llm-data-pipeline-debugger.git
   cd llm-data-pipeline-debugger
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file (optional if using OpenAI)**
   ```bash
   cp .env.example .env
   ```

5. **Run the debugger**
   ```bash
   python cli.py --config config.yaml
   ```

---

## 🧠 Example Use Case

You're debugging a pipeline that fails due to null values in a primary key. This tool will:
1. Analyze your log file and detect the probable root cause.
2. Run data validation against your dataset.
3. Combine both outputs to give a smart diagnosis and next steps (e.g., “drop null rows,” “reorder processing steps”).

---

## 🤖 Powered By

- [Google Gemini (Generative AI)](https://ai.google.dev/)
- [Great Expectations](https://greatexpectations.io/)
- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit (optional UI)](https://streamlit.io/)

---

## 📦 License

MIT © 2025 Or Benson  
Feel free to fork, extend, and customize!
```

---

Let me know if you want to auto-generate the full repo including sample files or Docker setup.
