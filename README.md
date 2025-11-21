# 🏭 Content Factory AI  
### Multi-Agent Content Automation System  
**Google × Kaggle Agents Intensive — Capstone Project 2025**  
**Track: Enterprise Agents**

---

## 🚀 Overview

Content Factory AI is a full end-to-end, multi-agent automation system that turns one topic into complete, platform-ready content. It mimics how real content teams work: research → write → fact-check → edit → optimize → analyze → finalize.

The system generates:

- Blog article  
- LinkedIn post  
- Twitter thread  
- Email newsletter  
- Video script  

All using a coordinated team of specialized agents.

No API keys required — fully offline & deterministic for Kaggle evaluation.

---

## 🤖 Multi-Agent Pipeline

```
User Input
    ↓
Research Agent
    ↓
Parallel Writer Agents (5 formats)
    ↓
Fact-Checker Agent
    ↓
Editor Agent
    ↓
SEO Agent
    ↓
Analytics Agent
    ↓
Output Generator
```

Each agent passes structured JSON, ensuring predictable results.

---

## 🗂 Project Structure

```
content-factory-ai/
│
├── src/                              # Source code
│   ├── agents/                       # Agent implementations
│   ├── tools/                        # Utility tools
│   ├── memory/                       # Memory systems
│   ├── utils/                        # Helpers / logging / metrics
│   ├── webui.py                      # Streamlit UI
│   ├── main.py                       # CLI entry
│   └── orchestrator.py               # Multi-agent orchestrator
│
├── tests/                            # Automated test suite
├── examples/                         # Example outputs
├── logs/                             # Runtime logs
├── memory/                           # Persistent memory store
├── docs/                             # Documentation
│
├── requirements.txt
├── setup.sh
├── setup.bat
├── README.md
└── LICENSE
```

---

## 🌟 Features

- Research-driven content generation  
- Multi-platform writing  
- Agent-based fact-checking  
- Editing + tone improvement  
- SEO optimization  
- Analytics (readability, sentiment)  
- Streamlit Web UI  
- No API keys required  
- Fully reproducible for Kaggle  

---

## 🛠 Install & Run

```bash
pip install -r requirements.txt
streamlit run src/webui.py
```

Or run CLI:

```bash
python src/main.py
```

---

## 📦 Sample Outputs

See `examples/sample_output/`

---

## 🏆 Kaggle Submission  
This project includes:

✔ Multi-agent system  
✔ Sequential + parallel agents  
✔ Tools + memory + orchestrator  
✔ Observability (logging & metrics)  
✔ Clean documentation  
✔ Fully deterministic offline mode  

---

## 📜 License  
MIT License  

