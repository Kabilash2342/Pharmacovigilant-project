# 💊 Agentic Pharmacovigilance Safety Intelligence System

An **Agentic AI-powered Pharmacovigilance (PV) system** that uses **MCP, LangGraph, LLMs, and SQL** to investigate drug safety cases and generate safety investigation reports.

The system allows a user to interact conversationally with a pharmacovigilance AI agent that can retrieve adverse events, investigate safety cases, access drug information, perform safety analytics, and generate structured safety investigation reports.

> **Note:** This project uses synthetic/mock pharmacovigilance data for demonstration and educational purposes. It is not intended for clinical or regulatory decision-making.

---

## 🚀 Features

- 🤖 **Agentic AI** using LangGraph
- 🔌 **MCP Server** for standardized tool access
- 💊 Drug information retrieval
- ⚠️ Adverse event investigation
- 🔎 Safety case search and analysis
- 📊 Safety analytics
- 📚 Literature search
- 🗄️ SQL-based pharmacovigilance database
- 📝 Automated Safety Investigation Report generation
- 💬 Conversational AI interface
- 🧪 MCP tool testing
- 📄 PDF and Markdown report generation

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              ┌───────────────┐
              │  AI Agent     │
              │  LangGraph   │
              └───────┬───────┘
                      │
                      ▼
               ┌─────────────┐
               │ MCP Client  │
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ MCP Server  │
               └──────┬──────┘
                      │
        ┌─────────────┼──────────────┐
        │             │              │
        ▼             ▼              ▼
  Adverse Event   Drug Info     Safety Database
      Tool           Tool            Tool
        │             │              │
        └─────────────┼──────────────┘
                      │
                      ▼
                PostgreSQL / SQL
                      │
                      ▼
             Safety Investigation
                    Report
```

---

## 🧠 Agent Workflow

The agent receives a pharmacovigilance query and determines which MCP tools are required.

Example:

```text
User
 │
 │ "Investigate liver injury associated with Drug X"
 ▼
Agent
 │
 ├── search_adverse_events()
 │
 ├── get_drug_information()
 │
 ├── query_safety_database()
 │
 ├── safety_analytics()
 │
 └── search_literature()
          │
          ▼
    Agent synthesizes
       the results
          │
          ▼
 Safety Investigation Report
```

---

## 🔌 MCP Tools

The MCP server exposes specialized tools for pharmacovigilance tasks.

### Adverse Event Tools

```text
search_adverse_events()
```

Searches adverse event records based on drug or event information.

### Drug Information

```text
get_drug_information()
```

Retrieves information about a drug and its associated safety information.

### Safety Database

```text
search_safety_cases()
query_safety_database()
```

Searches and analyzes safety case information stored in the database.

### Safety Analytics

```text
safety_analytics()
```

Provides aggregated safety information and identifies patterns requiring further human review.

### Literature Search

```text
search_literature()
```

Searches available literature/safety information relevant to a case.

---

## 📁 Project Structure

```text
Pharmacovigilant-project/
│
├── agent/
│   ├── __init__.py
│   └── graph.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema.sql
│   └── seed.py
│
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   └── tools/
│       ├── __init__.py
│       ├── adverse_events.py
│       ├── drug_information.py
│       ├── literature_search.py
│       ├── safety_analytics.py
│       └── safety_database.py
│
├── reports/
│
├── test/
│   ├── __init__.py
│   ├── mcp_test.py
│   └── tools.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Technology                  | Purpose                    |
| --------------------------- | -------------------------- |
| Python                      | Core development           |
| LangGraph                   | Agent orchestration        |
| MCP                         | Tool integration           |
| LLM                         | Natural language reasoning |
| SQL                         | Safety database            |
| FastAPI / Application Layer | Backend integration        |
| Streamlit                   | User interface             |
| PDF generation              | Safety reports             |

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Kabilash2342/Pharmacovigilant-project.git
cd Pharmacovigilant-project
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file containing your API credentials.

Example:

```text
GROQ_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

**Never commit `.env` or API keys to GitHub.**

---

## ▶️ Running the Application

Run the application using:

```bash
python app.py
```

Follow the application's interface to interact with the pharmacovigilance agent.

---

## 🧪 Testing

Run the MCP tests using:

```bash
python -m pytest
```

or run the individual test scripts as required.

---

## 📄 Example Output

The system can generate a structured Safety Investigation Report containing:

```text
Safety Investigation Report

Case Information
Drug Information
Adverse Events
Patient Information
Seriousness
Historical Safety Cases
Safety Analytics
Literature Findings
Investigation Summary
```

The generated reports are based on **synthetic data** for demonstration.

---

## 🔒 Safety & Data Disclaimer

This project is intended for **educational and portfolio demonstration purposes**.

It does not provide medical advice, diagnose patients, establish drug-event causality, or replace professional pharmacovigilance assessment.

All demonstrated patient and safety-case information should be treated as synthetic/mock data.

---

## 👨‍💻 Author

**Kabilash B**

AI/ML Engineer | Generative AI | Agentic AI | Pharmacovigilance AI

GitHub:  
https://github.com/Kabilash2342
