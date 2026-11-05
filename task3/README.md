# Task 3 – Authentication and Authorization

Roles:
- Employee: can view employee records.
- Administrator: can view, add, update and delete employee records.
All `/employees` routes require a JWT access token.

Demo accounts (created automatically):
- Employee: `employee1` / `Employee@123`
- Administrator: `admin1` / `Admin@123`

This task has its own virtual environment and dependency list, so it can be run
without installing packages for the other tasks.

From this folder (`task3`), set it up once:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the API from this folder:
```bash
.\.venv\Scripts\python.exe app.py
```
API: `http://127.0.0.1:5003`

Unauthenticated request (401):
```bash
curl -i http://127.0.0.1:5003/employees
```

Employee login:
```bash
curl -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d "{\"username\":\"employee1\",\"password\":\"Employee@123\"}"
```
Copy `access_token` from the response and use it:
```bash
curl http://127.0.0.1:5003/employees -H "Authorization: Bearer PASTE_EMPLOYEE_TOKEN"
```
Employee trying to add (403):
```bash
curl -i -X POST http://127.0.0.1:5003/employees -H "Authorization: Bearer PASTE_EMPLOYEE_TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Sara Ahmed\",\"department\":\"IT\",\"email\":\"sara@example.com\"}"
```

Administrator login:
```bash
curl -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d "{\"username\":\"admin1\",\"password\":\"Admin@123\"}"
```
Use the admin token to create:
```bash
curl -X POST http://127.0.0.1:5003/employees -H "Authorization: Bearer PASTE_ADMIN_TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Sara Ahmed\",\"department\":\"IT\",\"email\":\"sara@example.com\"}"
```
Update/delete using the returned employee ID:
```bash
curl -X PUT http://127.0.0.1:5003/employees/1 -H "Authorization: Bearer PASTE_ADMIN_TOKEN" -H "Content-Type: application/json" -d "{\"department\":\"Software Engineering\"}"
curl -X DELETE http://127.0.0.1:5003/employees/1 -H "Authorization: Bearer PASTE_ADMIN_TOKEN"
```
Invalid login (401):
```bash
curl -i -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d "{\"username\":\"employee1\",\"password\":\"incorrect\"}"
```

Authentication verifies identity at login and issues a JWT. Authorization checks the role in that token. A valid Employee token can read but receives HTTP 403 for administrator-only write operations.

Demo checklist:
- [ ] Unauthenticated access is rejected.
- [ ] Invalid credentials are rejected.
- [ ] Employee can view records.
- [ ] Employee cannot create/update/delete.
- [ ] Administrator can create/update/delete.
