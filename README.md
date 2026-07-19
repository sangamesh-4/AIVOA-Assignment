# AI-First CRM Healthcare Professional (HCP) Interaction Module

[cite_start]An intelligent, split-screen Customer Relationship Management (CRM) Log Interaction screen tailored for life science field representatives[cite: 7, 9, 10]. [cite_start]This application replaces cumbersome manual data entry workflows by utilizing a stateful conversational AI Assistant to dynamically control, populate, and refine structured records[cite: 12].

## 🚀 Tech Stack
* [cite_start]**Frontend:** React UI with structured application state tracking[cite: 13].
* [cite_start]**Backend:** Python with FastAPI framework primitives[cite: 14].
* [cite_start]**AI Agent Framework:** LangGraph state machine workflow graphs[cite: 15].
* [cite_start]**Large Language Model (LLM):** Groq API Layer hosting the `gemma2-9b-it` foundation framework[cite: 16].
* [cite_start]**Typography:** Google Inter font family baseline[cite: 19].

---

## 🌐 LangGraph Agent Architecture

[cite_start]The backend utilizes **LangGraph** to construct a stateful orchestrator that governs the lifespan of HCP interaction records[cite: 15, 26]. [cite_start]Instead of single-turn stateless prompt executions, the agent tracks conversational history and maintains form values inside an active Graph State object[cite: 26].

### Core Agent Capabilities:
* [cite_start]**State Persistence:** Preserves form information across multiple turns, enabling seamless context management[cite: 26].
* [cite_start]**Intelligent Routing:** Analyzes incoming unstructured statements or corrections and branches execution to target execution tool nodes dynamically[cite: 26].
* [cite_start]**Downstream Text Merging:** Mutates deep localized parameters (such as strings embedded inside an Outcomes narrative text box) based on follow-up user corrections[cite: 26, 30].

---

## 🛠️ Implemented LangGraph Agent Tools

[cite_start]The system architecture implements 5 distinct functional tools to manage CRM pipeline workflows[cite: 27]:

1.  [cite_start]**`log_interaction` (Required):** Extracts key data entities (HCP Name, Date, Attendees) from raw conversational entries and performs abstractive text summarization to write structured discussion updates[cite: 29].
2.  [cite_start]**`edit_interaction` (Required):** Inspects the active Graph State to safely adjust localized parameters based on user modifications without clearing the remaining form fields[cite: 30].
3.  **`infer_sentiment`:** Classes the underlying tone of user remarks to map state tracking to strict metrics: `Positive`, `Neutral`, or `Negative`.
4.  **`search_and_add_materials`:** Matches natural language asset mentions against a localized digital repository to automatically attach valid reference standard chips (e.g., `OncoBoost Phase III PDF`).
5.  **`suggest_follow_ups`:** Cross-references outcomes against a tactical sales playbook to generate quick-action hyperlinked shortcuts at the base of the UI layout.

---

## 📁 Project Directory Structure
```text
AIVOA-Assignment/
├── frontend/                 # React Application Interface
│   ├── src/
│   │   ├── App.js            # Dual-column Controlled CRM Core UI
│   │   └── index.js
│   ├── package.json
│   └── public/
├── backend/                  # Python FastAPI Layer
│   ├── server.py             # LangGraph Core Orchestrator & Tool Nodes
│   └── requirements.txt
├── .gitignore                # Production Cache Filters
└── README.md                 # System Architectural Documentation
