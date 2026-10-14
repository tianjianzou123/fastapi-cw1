# FastAPI Presentation Guide

This guide supports the 15-minute group presentation. Slides 14 and 15 are backup slides and are not part of the planned running time.

## Four-presenter timing

| Presenter | Slides | Focus | Target time |
|---|---:|---|---:|
| Presenter 1 | 1–3 | Introduction, FastAPI overview and request flow | 3:00 |
| Presenter 2 | 4–6 | Scenario, REST endpoints and route code | 3:30 |
| Presenter 3 | 7–9 | Validation, two-minute live demo and tests | 4:00 |
| Presenter 4 | 10–13 | Evaluation, suitability, conclusion and references | 3:10 |
| Buffer | — | Handover and technical delay | 1:20 |

Each slide also contains speaker notes with concise talking points, transitions, timing and sources.

## Online learning resource

- GitHub Pages: https://tianjianzou123.github.io/fastapi-cw1/
- Repository: https://github.com/tianjianzou123/fastapi-cw1

Slide 12 shows the Pages address and a QR code. Test the QR code on a phone before class and keep the URL ready to paste into the Teams chat if requested.

## Start the demonstration before presenting

From the `fastapi-project` folder:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app
```

Open `http://127.0.0.1:8000/docs` and leave the browser on Swagger UI.

## Two-minute live demonstration

1. Expand `GET /tasks`, select **Try it out**, then **Execute**. Confirm `200` and `[]`.
2. Expand `POST /tasks`, select **Try it out**, paste the valid body below, then **Execute**. Confirm `201`.

```json
{
  "title": "Rehearse the demo",
  "status": "todo",
  "priority": 5
}
```

3. Change `priority` to `9` and execute again. Confirm `422` and point to the priority constraint.
4. Stop the live demonstration. Do not demonstrate update or delete unless the tutor asks.

## Fallback plan

If the server or browser fails, return to slide 8 and explain the expected `200`, `201` and `422` results. Slide 14 shows the complete CRUD flow, and slide 9 shows the verified `8 passed` test result. Do not spend presentation time troubleshooting.

## Before class

- Add the group members' names to the title slide if required by the tutor.
- Confirm the presentation order and practise speaker handovers.
- Run `pytest -q` and confirm `8 passed`.
- Start Uvicorn and open `/docs` before screen sharing begins.
- Keep the PowerPoint file, repository folder and browser available locally.
- Confirm the actual presentation slot and final link-submission deadline in Aula.
