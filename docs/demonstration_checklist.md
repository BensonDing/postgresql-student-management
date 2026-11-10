# Demonstration and final submission checklist

Check boxes yourself after completing the actions. Generated files are ready for review; unchecked local recording, publication and submission steps still require your action.

## Local setup

- [ ] Extract the entire project and install Python, PostgreSQL and pgAdmin 4.
- [ ] Create `student_management` using `create_database.sql`, connected to `postgres` with Auto-commit on.
- [ ] Connect to `student_management` and execute `init.sql` once (or schema + seed as the alternative).
- [ ] Confirm the table has INTEGER identity primary key, required TEXT names, required UNIQUE TEXT email, and nullable DATE.
- [ ] Confirm exactly John Doe / `john.doe@example.com` / `2023-09-01`, Jane Smith / `jane.smith@example.com` / `2023-09-01`, and Jim Beam / `jim.beam@example.com` / `2023-09-02`.
- [ ] Create `.venv`, install `requirements.txt`, and configure a private `.env` with your local values.
- [ ] Run `src/main.py`; option 1 shows the initial three records.
- [ ] Run `tests/integration_test.py` locally if using a role with CREATEDB privilege; confirm 15 tests pass. If you cannot run it, do not claim a successful local test.

## Recording preparation

- [ ] Prepare pgAdmin schema and SELECT tabs, PowerShell, and the code editor.
- [ ] Keep Auto-commit enabled in the pgAdmin verification Query Tool.
- [ ] Start with exactly the three required students; remove only rehearsal data or deliberately use the clearly marked rehearsal reset.
- [ ] Make terminal and pgAdmin text readable; ensure all five result columns are visible.
- [ ] Test microphone audio and full-screen capture across window switches.
- [ ] Close `.env`, password prompts, notifications and unrelated windows.
- [ ] Rehearse the English script with a stopwatch; target around 4:30, maximum 5:00.

## Required video evidence

- [ ] Introduce the PostgreSQL/Python application.
- [ ] Show the actual database, table, five fields, data types and constraints in pgAdmin.
- [ ] Show the three required initial records.
- [ ] Run option 1 / `getAllStudents()` and show all records.
- [ ] Run option 2 / `addStudent(...)` for Alex Chen and note the real generated ID.
- [ ] Immediately re-run SELECT in **pgAdmin** and show four records including Alex.
- [ ] Run option 3 / `updateStudentEmail(...)` for that same actual ID.
- [ ] Immediately re-run SELECT in **pgAdmin** and show `alex.chen.updated@example.com` on Alex's row.
- [ ] Run option 4 / `deleteStudent(...)` for that same actual ID.
- [ ] Immediately re-run SELECT in **pgAdmin** and show Alex removed, leaving the three initial students unchanged.
- [ ] Briefly show the Python connection, parameterized SQL, context-managed transactions and errors.
- [ ] Give a short conclusion and stop recording.
- [ ] Play back the entire video; confirm audible narration, readable results, and duration **no greater than 5 minutes**.

## GitHub and Brightspace submission

- [ ] Upload the video and obtain a link viewable by the grader without an access request.
- [ ] Replace the README's `NOT YET RECORDED` video placeholder with the actual video URL.
- [ ] Create a **new PUBLIC GitHub repository** for the assignment.
- [ ] Commit/upload README, requirements, `.gitignore`, `.env.example`, `database/`, `src/`, `docs/`, and `tests/` with their folder structure intact.
- [ ] Confirm there are no real credentials, `.env`, `.venv`, caches, database cluster files or unrelated personal files in GitHub.
- [ ] Confirm `README.md`, `database/`, and `src/` are at the repository root; do not upload only the project ZIP.
- [ ] Open the public repository while signed out; test the README's video link in a private window.
- [ ] Submit the **public GitHub repository URL** through **Brightspace**.
- [ ] Check the course deadline and save the Brightspace confirmation. The provided TA notes specify **-10% for late submissions**; the screenshots did not supply a deadline.

## Submission status supplied with this package

- Project code, SQL, documentation and test suite: created.
- Actual real PostgreSQL test run: **15/15 passed**, PostgreSQL 16.2 on Linux.
- Local Windows 11 / your pgAdmin GUI: **requires your verification**.
- Student-recorded video and real video URL: **not yet created**.
- Public GitHub repository and Brightspace submission: **not yet completed**.

