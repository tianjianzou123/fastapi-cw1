# FastAPI Presentation Guide

This guide supports the 15-minute COMP10020 group presentation. The group's final deck contains 18 slides: slides 1–17 are the planned presentation and slide 18 lists references.

## Four-presenter timing

| Presenter | Slides | Focus | Target time |
|---|---:|---|---:|
| Member 1 | 1–4 | Introduction, FastAPI overview, key features and architecture | 2:55 |
| Member 2 | 5–8 | HTTP example, scenario, CRUD and status codes | 3:00 |
| Member 3 | 9–12 | Route code, Pydantic validation and live demonstration | 3:55 |
| Member 4 | 13–17 | Testing, advantages, limitations, use cases and conclusion | 3:25 |
| Buffer | — | Handover, slide changes and a small technical delay | 1:00 |

The planned content and demo total about 13 minutes 15 seconds. The buffer keeps the classroom presentation below 15 minutes.

## Final presentation files

- `FastAPI_Task_Manager_Presentation_Final.pptx` — the group's 18-slide final deck with embedded speaker notes; slide 13 contains the test command and summary
- `PRESENTATION-GUIDE.md` — timing, handover, live-demo and fallback guidance for the group

## Online learning resource

- GitHub Pages: https://tianjianzou123.github.io/fastapi-cw1/
- Public repository: https://github.com/tianjianzou123/fastapi-cw1

Slide 17 contains the Pages URL and a QR code. Test both before class and keep the URL ready to paste into Microsoft Teams if requested.

## Start the demonstration before presenting

From the `fastapi-project` folder:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app
```

Open `http://127.0.0.1:8000/docs` and leave the browser on Swagger UI before the presentation begins.

## Live demonstration on slide 12

Keep the live section to about 2 minutes 15 seconds:

1. Expand `GET /tasks`, select **Try it out**, then **Execute**. Point to `200 OK` and the JSON list.
2. Expand `POST /tasks`, select **Try it out**, paste the valid body below, then **Execute**. Point to `201 Created` and the returned task ID.

```json
{
  "title": "Rehearse the demo",
  "status": "todo",
  "priority": 5
}
```

3. In the same `POST /tasks` request, change `priority` to `9` and execute again. Point to `422 Validation Error` and explain that Pydantic accepts only values from 1 to 5.
4. Return to the PowerPoint. Do not demonstrate update or delete unless the tutor asks.

## Automated testing on slide 13

Allow 35–40 seconds within Member 4's allocated time. Open a prepared second PowerShell window in `fastapi-project` and run:

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

Expected result: `8 passed`. Point to the result, explain that TestClient uses a fresh repository for each test, and return to slide 14. Uvicorn can stay open. The elapsed test time varies. Passing tests support the checked cases; they do not prove that every possible bug is absent.

## Fallback plan

If the server or browser fails, return to slide 12 and explain the expected `200`, `201` and `422` results shown on the slide. Slide 13 summarises the test coverage and verified eight-test result. If the terminal fails, explain this summary and continue. Do not spend presentation time troubleshooting.

## Before class

- Review the completed Group E submission form and shared declaration before uploading both Word files.
- Confirm the speaking order and practise handovers.
- Run `pytest -q` and confirm `8 passed`.
- Start Uvicorn and open `/docs` before screen sharing begins.
- Test the GitHub Pages link and QR code on a second device.
- Keep the PowerPoint, browser and repository available locally.
- Confirm the exact presentation slot and submission deadline in Aula.

