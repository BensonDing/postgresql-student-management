# Actual verification report

**Run date:** November 10, 2026. These are actual execution results, not predicted results or screenshots of invented data.

## Verified runtime

| Component | Observed value |
| --- | --- |
| Operating system | Linux (execution environment), not Windows 11 |
| Python | 3.12.14 |
| PostgreSQL server | 16.2, actual PostgreSQL server process |
| Psycopg | 3.3.8, binary implementation |
| python-dotenv | 1.2.2 |
| Database isolation | Unique disposable `student_crud_test_...` database, dropped after tests |
| Test result | **15 tests passed; 0 failures; 0 errors** |

PostgreSQL binaries were made available through a development-only `pgserver` package. The tests connected over loopback TCP to the real PostgreSQL server, not a mock, SQLite database, browser service or in-memory simulator. `pgserver` is not an application dependency and is not needed on Windows; use your regular PostgreSQL installation there. The disposable local test server used trust authentication, so password-authentication setup was not validated here.

Observed test summary:

```text
Real PostgreSQL server version: 16.2
Ran 15 tests in 1.290s
OK
```

## Tests actually passed

| Test | What the real execution established |
| --- | --- |
| 01 Initial records and display | Exact names, emails, dates, starting IDs; all rows/header/count displayed |
| 02 Column types / identity | Five correct columns, INTEGER/TEXT/DATE, correct nullability and identity |
| 03 Add commit / ID | New generated ID; independent connection sees committed insertion |
| 04 Update target | Only selected student's email changes; seeds unchanged |
| 05 Delete target | Selected test row removed; original three rows remain |
| 06 Duplicate insert | UNIQUE rejects insert; rollback preserves rows; next valid call succeeds |
| 07 Duplicate update | UNIQUE rejects email change; old values remain |
| 08 NOT NULL | PostgreSQL rejects NULL first name, last name and email |
| 09 Primary key | PostgreSQL rejects duplicate and NULL student IDs |
| 10 Nullable date | Both None and blank application inputs persist SQL NULL |
| 11 Invalid input | Bad dates, missing text, invalid IDs produce safe failure without writes |
| 12 Missing IDs | Update/delete return False and explain no record was found |
| 13 Parameterized values | Apostrophes and SQL-like names are stored literally; table remains intact |
| 14 Connection/configuration errors | Real wrong-database/closed-port failures and invalid port configuration handled; subsequent valid connection succeeds |
| 15 Actual interactive CLI | Subprocess input performs read/add/update/delete, rejects bad menu choice, and exits cleanly at end-of-input |

Every normal CRUD write was verified through a separate database connection. The source contains no simulated database operations. Tests used a separate database; no user's existing assignment data was modified.

## Additional package checks actually completed

- Executed **all six SQL files** against real PostgreSQL: database creation, combined initialization, verification SELECT, optional rehearsal reset, and the alternative schema/seed route.
- Ran the English script's exact Alex Chen inputs through actual CLI subprocesses. Separate connection readbacks confirmed the sequence **3 → 4 → 4 → 3**, the updated email, and restoration of the unchanged seed rows. The fresh demo ID was 4 in this smoke check; use the actual ID on your computer.
- Confirmed that combined initialization and separate schema/seed files contain identical executable statements.
- Checked Python syntax and local Markdown links.
- Downloaded compatible **Windows x64 / CPython 3.12** dependency wheels using the pinned requirements. This verifies package availability, not execution on Windows.
- Confirmed `.gitignore` excludes `.env`, `.env.local`, virtual-environment content and Python bytecode. The public package contains only the example password `CHANGE_ME`.

## Not yet verified here

- Execution on the student's Windows 11 installation, PostgreSQL service and chosen password.
- Visual pgAdmin 4 checks on the student's computer, including the three live changes in the video.
- The student's microphone/screen capture, speaking pace, final video length and uploaded link access.
- Public GitHub repository creation, actual commits, or Brightspace submission.

The GitHub connector could read the connected profile but offered no repository-creation action. The browser repository-creation page required authentication, and the local GitHub CLI was not signed in. **No public repository was created or published.**

## Exact local verification procedure (Windows 11)

1. Follow README sections 1–4 to install, create the database, execute `init.sql`, install requirements and configure `.env`.
2. From the project root run:

   ```powershell
   .\.venv\Scripts\python.exe .\tests\integration_test.py
   ```

   Use the local `postgres` role (or a role with CREATEDB); verify the output ends with 15 tests and `OK`. If not, resolve the actual error before recording. Do not assume the Linux result proves your Windows configuration.
3. Run the app:

   ```powershell
   .\.venv\Scripts\python.exe .\src\main.py
   ```

4. In pgAdmin's `student_management` Query Tool, open `database/verify.sql`, enable Auto-commit and press F5. Verify the exact three seeds.
5. Use option 1; then option 2 with Alex Chen / `alex.chen@example.com` / `2024-01-15`. Note the actual generated numeric ID. Re-run the pgAdmin SELECT: four rows.
6. Use option 3 with that ID and `alex.chen.updated@example.com`. Re-run SELECT: four rows, Alex's email changed, original seeds unchanged.
7. Use option 4 with the same ID. Re-run SELECT: only the original three rows remain.
8. Optional manual error check: attempt to add a student using `john.doe@example.com`. Expect a duplicate-email error and no new row; then option 1 must still work. A rejected insert can advance the identity sequence without adding a row.
9. Record the demonstration only after these local checks succeed. The final checklist covers upload and submission.

