---
applyTo: '**'
---
Provide project context and coding guidelines that the AI should follow when generating code, answering questions, or reviewing changes.

### 1. Project Context

-   **Project Name**: AI-Driven Learning Platform (Mini MVP).
-   **Objective**: A full-stack application where users select a category and sub-category, submit a text prompt, receive a generated lesson from an AI, and can view their learning history.
-   **Core Technologies**:
    -   **Backend**: **Python with FastAPI**. It uses SQLAlchemy as the ORM and Alembic for database migrations.
    -   **Frontend**: **React (built with Vite)**. It uses JavaScript and the `axios` library for making API calls.
    -   **Database**: **PostgreSQL**, managed via **Docker Compose** (ensuring a consistent, isolated environment and avoiding reliance on a local installation).
    -   **AI Integration**: The backend communicates with the Google Gemini API using the `google-generativeai` Python library.
-   **Project Structure**: This is a monorepo with two main directories:
    -   `backend/`: Contains the entire FastAPI application, including its own `.venv` virtual environment.
    -   `frontend/`: Contains the entire React application.

-   Read and follow the PROJECT_STRUCTURE.md file in this repository for detailed architecture, file structure, database schema, and implementation guidelines
### 2. Workspace & Workflow Instructions

**CRITICAL: Always follow these steps when performing tasks in the terminal.**

-   **For Backend Development**:
    1.  First, navigate into the backend directory: `cd backend`
    2.  **Activate the Python virtual environment** located at `backend/.venv`. The activation command is typically `.\.venv\Scripts\Activate.ps1` for PowerShell or `source .venv/bin/activate` for Bash/Zsh.
    3.  Key commands: `pip install -r requirements.txt`, `uvicorn main:app --reload`.
    4.  **Database Migrations (Alembic)**: This project uses Alembic to manage database schema changes.
        -   When a SQLAlchemy model in `models.py` is modified, a migration script must be generated:
          `alembic revision --autogenerate -m "A short, descriptive message about the change"`
        -   To apply the migration to the database: `alembic upgrade head`

-   **For Frontend Development**:
    1.  First, navigate into the frontend directory: `cd frontend`
    2.  If a Python virtual environment (`.venv`) is active, **you must deactivate it first** using the `deactivate` command.
    3.  Key commands: `npm install`, `npm run dev`.

### 3. Coding Guidelines

-   **General**:
    -   Follow best practices for clean, modern, readable, and maintainable code. Use meaningful names.
    -   Document complex logic with clear comments.
-   **Python (Backend)**:
    -   Adhere to PEP 8 standards. Use Pydantic models (`schemas.py`) for API validation. Use SQLAlchemy models (`models.py`) for database tables.
    -   Keep business logic in separate, dedicated files (`database.py`, `ai_service.py`).
-   **React (Frontend)**:
    -   Build with a component-based architecture (`src/components/`, `src/pages/`).
    -   Use functional components with React Hooks (`useState`, `useEffect`).
    -   **Styling**: Separate styling from logic. Create dedicated CSS files for components (e.g., `MyComponent.css`) and import them. Avoid inline styles. **Maintain a consistent visual theme** across all components. Define global styles in `index.css`.

### 4. AI Interaction & Safety

-   **Security**: Sensitive information (`GEMINI_API_KEY`, database credentials) must **never** be hardcoded. Load them from a `.env` file, and ensure `.env` is listed in the root `.gitignore`.
-   **Explanations**: When generating code, provide clear explanations for the changes.
-   **Error Handling**: Implement proper error handling for API calls, database transactions, and user input.