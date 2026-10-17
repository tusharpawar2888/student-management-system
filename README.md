# StudentHub — Student Management System

A responsive Flask website with SQLite storage, CRUD operations, search, JSON API, pytest tests, Flake8 checks, and a Jenkins CI pipeline. Docker is not used.

## Features
- Dashboard with student totals and course overview
- Create, list, search, edit, and delete students
- Validates required fields and email format
- Unique email addresses
- SQLite database created automatically
- API: `GET /api/health`, `GET /api/students`, `POST /api/students`

## Run locally
Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Test and quality checks
```bash
python -m pytest -v
python -m flake8 app.py tests/test_app.py
```

## SQLite persistence
Default database is `students.db` in this project directory. Set `DATABASE_PATH` to change its location. The database is excluded from Git. For hosted deployment, make sure the provider offers persistent storage for SQLite, otherwise data may disappear when instances restart or redeploy.

## Jenkins
The included Jenkinsfile uses POSIX `sh` steps and therefore expects a Linux/Unix Jenkins agent. Your previous Jenkins setup was Windows; either configure a Linux agent or translate `sh` commands to `bat` before using this Jenkinsfile on Windows. It runs build, tests, Flake8 and packages the website. Live hosting deployment is not configured yet; add the hosting provider's deployment action only after configuring credentials securely.

Set a strong `SECRET_KEY` environment variable for deployment. This demo has no login/authentication, so do not use it for sensitive real student data without adding access controls.
