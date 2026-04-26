# 🎓 Multi-Agent Educational Assistant (MAS)
An autonomous, locally-hosted Multi-Agent System designed to transform raw lecture notes into structured study materials. Built using **LangGraph**, **LangChain**, and **Ollama (Llama 3)**, this system automates the pedagogical workflow from content perception to personalized remedial planning.

---

## 🌟 Key Features
- **Local Inference:** Powered by Llama 3 via Ollama for 100% data privacy and zero API costs.
- **Stateful Orchestration:** Utilizes a sequential LangGraph pipeline with a shared `AgentState`.
- **High Observability:** Centralized logging system (`logs.txt`) providing a full audit trail of agent reasoning.
- **Persistence Layer:** Automated tools to extract data from `.txt` and persist outputs to `.json` and `.txt` files.

---

## 🏗 System Architecture
The system operates as a **Sequential Pipeline**, where each agent refines the state before passing it to the next:

1. **Content Summarizer (The Professor):** Distills lecture notes into a professional abstract.
2. **Quiz Generator (The Senior Examiner):** Synthesizes 3 challenging MCQs from the summary.
3. **Performance Evaluator (The Academic Evaluator):** Grades student understanding and identifies knowledge gaps.
4. **Study Planner (The Study Consultant):** Generates a tailored 7-day intensive study schedule.

---

## 📂 Project Structure
```text
├── agents.py           # Persona-based logic for the 4 AI Agents
├── tools.py            # Custom Python tools for robust File I/O
├── state.py            # TypedDict definition for the Global AgentState
├── main.py             # LangGraph workflow definition & execution entry point
├── logger_config.py    # Centralized logging configuration (Observability)
├── test_all.py         # Automated unit tests and assertions
├── notes.txt           # Input layer: Source lecture notes
└── logs.txt            # System execution traces (Auto-generated)

🚀 Getting Started
1. Prerequisites
Python 3.10+

Ollama: Download here

Llama 3 Model: Run the following command in your terminal:

Bash
ollama pull llama3
2. Installation
Clone this repository and install the required dependencies:

Bash
pip install -r requirements.txt
3. Execution
Place your lecture content in notes.txt.

Run the Multi-Agent System:

Bash
python main.py
View the generated outputs in summary.txt, quiz.json, and study_plan.txt.

🛠 Individual Contribution (Student 1)
Responsible for the Data Ingress and Perception Layer:

Agent Design: Engineered the Summarizer Agent using a "Distinguished Professor" persona and conciseness constraints.

Tool Engineering: Developed the file_reader_tool and summary_saver_tool with strict type hinting and docstrings.

Problem Solving: Resolved UnicodeEncodeError by implementing UTF-8 encoding across all file-writing tools to support AI-generated symbols and emojis.

Observability: Integrated standardized logging to track tool execution status.

🧪 Testing
The system includes an automated test suite to verify agent logic and output integrity:

Bash
python test_all.py
