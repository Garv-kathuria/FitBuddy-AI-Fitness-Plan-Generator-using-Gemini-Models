# FitBuddy AI 🏋️‍♂️

FitBuddy AI is a generative AI-powered web application that creates highly personalized 7-day workout routines and targeted nutrition tips based on user profiles. It features a dynamic feedback loop, allowing users to tweak and regenerate their plans on the fly.

## 👥 Team & Milestones Completed

This project was developed by dividing core milestones across the team:

* **Milestone 1: Model Selection and Architecture**
    * *Activity 1.1:* Researched and integrated Google Gemini 2.5 Flash via the modern `google-genai` SDK.
    * *Activity 1.2:* Defined an MVC-style architecture.
    * *Activity 1.3:* Set up the Python virtual environment and `requirements.txt`.
* **Milestone 2 & 3: Core Functionalities & Backend** 
    * *Activity 2.1 & 2.2:* Built the SQLite database integration using SQLAlchemy and data validation using Pydantic (`models.py`, `schemas.py`, `database.py`).
    * *Activity 3.1:* Developed the main application logic and routing in `routes.py`, handling form submissions and AI service calls.
* **Milestone 4 & 5: Frontend & Deployment** 
    * *Activity 4.1 & 4.2:* Designed the responsive UI and created dynamic HTML templates using Jinja2 and Markdown parsing (`base.html`, `index.html`, `result.html`).
    * *Activity 5.1 & 5.2:* Configured the Uvicorn ASGI server for local deployment, successfully tested endpoints, and handled API rate-limit debugging.

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** SQLite + SQLAlchemy ORM
* **AI Integration:** Google GenAI SDK (Model: `gemini-2.5-flash`)
* **Frontend:** HTML5, CSS3, Jinja2 Templates, Python-Markdown

## 📂 Project Structure

```text
fitbuddy/
├── .env                  # (Not tracked in Git) Stores GEMINI_API_KEY
├── requirements.txt      # Project dependencies
├── main.py               # FastAPI app initialization and DB creation
├── routes.py             # Web endpoints (GET /, POST /generate, POST /feedback)
├── database.py           # SQLite connection setup
├── models.py             # SQLAlchemy database tables (User, WorkoutPlan)
├── schemas.py            # Pydantic models for data validation
├── ai_generator.py       # Google Gemini API connection and prompt logic
└── templates/            # Jinja2 HTML templates
    ├── base.html         # Master layout and CSS
    ├── index.html        # User input form
    └── result.html       # AI output and feedback loop