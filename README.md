# CSC3109 Software Engineering – Assignment 1

This project implements all three tasks in the supplied assignment PDF.

## Requirements and installation
- Python 3.10+
- pip
- cURL for API testing
- SQLite does **not** need a separate installation: Python includes `sqlite3` in its standard library. Each database is created automatically.
- Optional SQLite GUI: DB Browser for SQLite, https://sqlitebrowser.org/

Each task can be installed and run independently. In a terminal, first enter
the task folder you want to run (for example, `cd task1`), then create its
virtual environment and install that task's requirements:

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The commands above are for Windows. On macOS/Linux, use
`./.venv/bin/python -m pip install -r requirements.txt` instead.

Alternatively, to use one shared environment for all tasks, run this from the
project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

From a task folder, explicitly run the root interpreter as
`..\.venv\Scripts\python.exe app.py` (or activate the root environment first).
Installing into a virtual environment does not install packages for a
separate, system-level `python`.

## Run tasks from the project root (Windows)
If you installed dependencies into the root `.venv` as shown above, stay in
the project root and run:

Task 1 API:
```powershell
.\.venv\Scripts\python.exe .\task1\app.py
```
Task 1 Streamlit frontend (in a second terminal):
```powershell
.\.venv\Scripts\python.exe -m streamlit run .\task1\streamlit_app.py
```

Task 2:
```powershell
.\.venv\Scripts\python.exe .\task2\app.py
```

Task 3:
```powershell
.\.venv\Scripts\python.exe .\task3\app.py
```

Alternatively, if you created a separate `.venv` inside each task folder,
follow that task's README and run its commands from inside that task folder.

## Task 1 – Student API + Streamlit
Flask: http://127.0.0.1:5001 | Streamlit: http://localhost:8501

## Task 2 – API keys
The first run generates three unique keys and writes them to
`task2/secrets/api_keys.txt`. Share them privately with testers; do not commit
this file. API: http://127.0.0.1:5002.

## Task 3 – Authentication and authorization
API: http://127.0.0.1:5003.
Demo employee: `employee1` / `Employee@123`
Demo administrator: `admin1` / `Admin@123`

These are classroom-only credentials. Change them before deployment.

## Submission / video
The assignment PDF requires code and a video demonstration (or public video link) in each task folder. Source code and demo checklists are included, but no video is recorded by this project. Record your own demonstration and add the video or public link to the relevant task README. Push to a public Git repository, but never commit generated API keys, database files, tokens, `.env`, or virtual environments. Put your public repository URL in `repository_link.txt`.

## Runtime databases
Automatically created: `task1/students.db`, `task2/apikeys.db`, `task3/employees.db`. Delete a database to reset that task's local data.
