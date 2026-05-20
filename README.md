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
