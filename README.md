# FastAPI Task Manager

A beginner-friendly learning project for the COMP10020 Internet Technologies FastAPI group presentation. It combines a small REST API, automated tests, presentation slides, online information and step-by-step tutorial lab instructions.

## Live links

- Online learning resource: https://tianjianzou123.github.io/fastapi-cw1/
- Public GitHub repository: https://github.com/tianjianzou123/fastapi-cw1

## Repository contents

- `fastapi-project/` — working FastAPI application and tests
- `docs/` — static learning resource for GitHub Pages
- `presentation/` — final PowerPoint presentation
- `requirements.txt` — application dependencies
- `requirements-dev.txt` — application and test dependencies

## Set up on Windows

Run these commands from the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Run the API

```powershell
cd fastapi-project
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open these local URLs after the server starts:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

The classroom demonstration uses only three actions in Swagger UI: list tasks, create one valid task, then send an invalid priority to show the automatic `422` response.

## Run the tests

From `fastapi-project/`:

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

Expected result: `8 passed`.

## Preview the learning resource

Open `docs/index.html` directly, or run a local static server from the `docs/` folder:

```powershell
python -m http.server 4173
```

Then open `http://127.0.0.1:4173`.

## GitHub Pages configuration

The online learning resource is served from the `docs/` folder on the `main` branch. To check or restore the configuration:

1. Open the repository **Settings**.
2. Select **Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the main branch and the `/docs` folder.
5. Save and wait for GitHub to display the public Pages URL.

Use the two live links above in the CW1 submission form.

