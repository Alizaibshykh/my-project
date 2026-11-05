# Task 1 – Student Management API and Streamlit

This task has its own virtual environment and dependency list, so it can be run
without installing packages for the other tasks.

From this folder (`task1`), set it up once:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the API in Terminal 1:
```bash
.\.venv\Scripts\python.exe app.py
```

Start the Streamlit frontend in Terminal 2, also from this folder:
```bash
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Flask API: `http://127.0.0.1:5001`; Streamlit: `http://localhost:8501`.

Use the task's `.venv\Scripts\python.exe` to run the app after setup. A plain
`python` command can select a different Python installation that does not
contain these dependencies.

Endpoints:
- `GET /students` – list all
- `GET /students/<id>` – get one
- `POST /students` – add
- `PUT /students/<id>` – update
- `DELETE /students/<id>` – delete

cURL examples:
```bash
curl http://127.0.0.1:5001/students
curl -X POST http://127.0.0.1:5001/students -H "Content-Type: application/json" -d "{\"student_id\":\"STU-001\",\"name\":\"Ali Khan\",\"department\":\"Computer Science\",\"email\":\"ali@example.com\"}"
curl http://127.0.0.1:5001/students/1
curl -X PUT http://127.0.0.1:5001/students/1 -H "Content-Type: application/json" -d "{\"name\":\"Ali Ahmed\",\"department\":\"Software Engineering\",\"email\":\"ali.ahmed@example.com\"}"
curl -X DELETE http://127.0.0.1:5001/students/1
```

Demo checklist:
- [ ] Show the Streamlit table.
- [ ] Add a student.
- [ ] Update a student.
- [ ] Delete a student.
- [ ] Show records refreshing after each successful operation.
- [ ] Optionally test endpoints using cURL.

SQLite database `students.db` is created automatically.
