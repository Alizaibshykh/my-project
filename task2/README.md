# Task 2 – API Key Generation and Sharing

This task has its own virtual environment and dependency list, so it can be run
without installing packages for the other tasks.

From this folder (`task2`), set it up once:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the API from this folder:
```bash
.\.venv\Scripts\python.exe app.py
```
API: `http://127.0.0.1:5002`.

At first launch, three unique keys are generated with Python `secrets` and saved locally in `secrets/api_keys.txt`. The database stores only SHA-256 hashes. Give each key privately to its assigned tester. Never commit the key file.

Valid request (replace the placeholder with a key):
```bash
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: PASTE_KEY_1" -d "{\"text\":\"hello api\"}"
```
Repeat with keys 2 and 3.

Missing key (401):
```bash
curl -i -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -d "{\"text\":\"hello\"}"
```
Invalid key (401):
```bash
curl -i -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: wrong-key" -d "{\"text\":\"hello\"}"
```

Demo checklist:
- [ ] Show all three keys locally (hide them from public screenshots).
- [ ] Test each valid key.
- [ ] Show missing and invalid keys being rejected.
- [ ] Explain the `X-API-Key` header.
