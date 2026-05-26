# hr-agent-platform

# Project structure

hr-agent-platform/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point & routes
│   ├── core/
│   │   ├── config.py        # .env loading with Pydantic Settings
│   │   └── database.py      # SQLite connection & Audit Log logic
│   ├── agents/
│   │   ├── orchestrator.py  # Intent classification & routing
│   │   ├── sub_agents.py    # Scheduling, Leave, Compliance stubs
│   │   └── graph.py         # LangGraph state & node definitions
│   └── services/
│       ├── memory.py        # STM/LTM logic & Significance scoring
│       └── audit.py         # Append-only logging service
├── data/
│   └── hr_platform.db       # SQLite DB (ignore in git)
├── tests/                   # Test suite for API endpoints
├── .env                     # API keys & Database URL
├── .gitignore               # Exclude venv, .env, and __pycache__
└── requirements.txt         # Dependencies

# Multi-Agent HR Task Routing & Memory Engine

This platform leverages a modular, high-throughput backend built on **FastAPI** and **LangGraph** to process incoming HR natural language requests, isolate state variations across clean agent boundaries, and manage persistence seamlessly. It was developed as part of the technical challenge for the AI Intern opportunity at **ZeloraTech Pvt Ltd**.

---

## 1. System Architecture Overview

### Architectural Workflow
* **API Ingress:** Incoming payloads pass through a structural **Pydantic** validation layer where strings are sanitized (e.g., stripping dangerous script tags) and assigned a tracking UUID (`request_id`).
* **Orchestrator Routing:** The central Orchestrator uses structured LLM calls to output an **Intent Classification** (*Leave*, *Scheduling*, *Compliance*, or *Clarification*) along with a numerical confidence score. Requests falling below a defined threshold automatically route to a fallback handler.
* **Sub-Agent Execution:** Processing transitions state dynamically via **LangGraph** to the target execution node using isolated execution contexts, transaction retries, and clean error boundaries.
* **Data & Storage Tier:** Every single node transition writes sequentially to an append-only SQLite transaction table (`audit_log`), while business-critical context is parsed using automated significance logic and saved to Long-Term Memory (`ltm`).

---

## 2. Core Module Implementations & Design Justifications

### A. Intent Classification & Routing Engine
* **Fallback Strategy:** If the orchestrator’s classification confidence falls below `0.70`, the system routes the request to the `Clarification` sub-agent. This prevents misrouting and keeps the system from throwing unhandled code exceptions.
* **Failure Boundaries:** Exceptions within agent steps are wrapped in polite, human-readable response boundaries. Raw Python stack traces are actively suppressed and caught within the FastAPI exception handling middleware to protect internal system metrics.

### B. Two-Tier Memory System (STM & LTM)
* **Short-Term Memory (STM):** Implemented using stateful conversational threads natively managed inside the LangGraph state channel. Ephemeral data survives solely for the duration of the current session graph loop.
* **Long-Term Memory (LTM):** Persistent storage handled securely by **SQLite**.
* **Significance Scoring Logic:** Every request processed is evaluated by an algorithmic significance scoring function. If a request contains high-impact metrics (such as exact date ranges, medical declarations, or specific policy references), it receives an increased importance rating. Items scoring above `0.80` trigger a write into the persistent database table (`ltm`) to ensure relevant corporate memory is retained across entirely new sessions.

### C. Append-Only Audit Trail
* **Enforcement:** The database connector structure strictly bans `UPDATE` or `DELETE` statements on the `audit_log` table to ensure immutability.
* **Fields Captured:** Every row explicitly records:
  * `request_id` (UUID tracking token)
  * `timestamp` (UTC generation moment)
  * `node_name` (The active LangGraph node executing)
  * `state_data` (A fully frozen JSON snapshot of the system state at that exact split-second)

---

## 3. Bug Findings and Code Corrections

During system development and exploration of the starter codebase, the following architectural bugs were identified and completely resolved:

1. **State Mutation Glitch:** Fixed an issue where concurrent request dictionary configurations were leaking data across active threads by enforcing strict immutability patterns within the state node structures.
2. **SQL Transaction Lock:** Patched a bug where rapid log database writing occasionally dropped data by implementing an asynchronous, thread-safe pool manager for the SQLite connection lifecycle.
3. **Input Validation Vulnerability:** Discovered an entry vulnerability where non-sanitized input strings could pollute downstream prompts. Resolved this by building custom validator regex blocks inside the foundational Pydantic schema layers.

---

## 4. Engineering Trade-offs & Future Extensions

* **SQLite vs. Fully Distributed Clusters:** For this initial design phase, SQLite was chosen for its lightweight, local database speed and zero-configuration environment overhead. For massive enterprise scale, this should migrate to a cloud-hosted relational layer or a distributed key-value store to eliminate local storage bottlenecks.
* **Synchronous Thread Handlers:** The current system isolates agent tasks sequentially. Transitioning completely to full async queue patterns would scale performance under high concurrent user load, but was deprioritized here to protect predictable operational state tracking.

---

## 5. Setup Instructions for Local Development

Follow these steps exactly to run, build, and test this application on any local machine.

### Prerequisites
* **Python 3.11 or 3.12** installed locally.
* **Docker Desktop** installed and running.

### Option A: Local Python Setup (Without Docker)

1. Extract the source files zip archive and navigate into the main project folder:
   ```bash
   cd HR-AGENT-PLATFORM

### Create and trigger a clean virtual environment
    
    python -m venv .venv

    ### Activate on Windows (PowerShell):
    .\.venv\Scripts\activate

    ### Activate on Mac/Linux:
    source .venv/bin/activate



### Install the specific dependencies
    
    pip install -r requirements.txt

### Initialize the environment variables. Create a file named .env in the root folder and add the configuration

    OPENAI_API_KEY=your_actual_api_key_here
    DATABASE_URL=sqlite:///./data/hr_platform.db

### Boot up the local web server using Uvicorn

    uvicorn app.main:app --reload

- Visit http://127.0.0.1:8000/docs in your browser to verify the local interactive Swagger interface.

### Option B: Containerized Deployment (Using Docker)

1. Make sure Docker Desktop is open and running on your computer.
2. Build the optimized cached image layer using your terminal

    docker build -t hr-agent-platform-image .

3. Launch the container background process and link the network bridge ports

    docker run -d --name hr_platform_app -p 8000:8000 hr-agent-platform-image

4. Confirm successful deployment by verifying the following live outputs
- API Interactive Documentation UI: http://127.0.0.1:8000/docs
- Active Container Runtime Logs: docker logs hr_platform_app

## 6. Verification Test Script
Run this single-line command in your local PowerShell terminal to watch the multi-agent engine execute an end-to-end task pipeline live inside the container environment:

    Invoke-RestMethod -Uri "[http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)" -Method Post -ContentType "application/json" -Body '{"user_id": "emp_abc123", "message": "I need to request sick leave starting tomorrow for two days due to a high fever."}'