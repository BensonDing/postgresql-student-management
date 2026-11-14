# PostgreSQL Student Management

A Python command-line application for the **Database Interaction with PostgreSQL and Application Programming** assignment. It performs real SELECT, INSERT, UPDATE and DELETE statements against `public.students` in PostgreSQL. The four function names and parameter lists match the assignment exactly.

## Demonstration video URL — complete before submission

**Video URL: https://youtu.be/0G8yxR6qiOs


## Technologies

- PostgreSQL; tested here with a real PostgreSQL **16.2** server on Linux.
- Python **3.12** (64 bit recommended on Windows 11).
- Psycopg **3.3.8**, using its binary package for simple installation.
- python-dotenv **1.2.2** for local configuration.
- pgAdmin 4 for local database inspection and video verification.

Windows 11 and pgAdmin GUI execution must still be verified on your computer.

## Files

| File | Purpose |
| --- | --- |
| `src/main.py` | The four required functions, connection handling and CLI |
| `database/create_database.sql` | Create `student_management`, run separately |
| `database/init.sql` | Complete table + exact initial data, one transaction |
| `database/schema.sql`, `database/seed.sql` | Alternative two-file initialization |
| `database/verify.sql` | SELECT to re-run in pgAdmin after each change |
| `database/reset_demo.sql` | Optional, destructive reset of the assignment table for rehearsal |
| `.env.example`, `.gitignore` | Configuration template and credential exclusions |
| `requirements.txt` | Pinned Python dependencies |
| `tests/integration_test.py` | Real-database tests in a disposable temporary database |
| `docs/demonstration_script.md` | Timed English narration and exact screen actions |
| `docs/recording_guide_zh.md` | Chinese setup, recording and GitHub upload guide |
| `docs/demonstration_checklist.md` | Recording and final submission checklist |
| `docs/requirements_traceability.md` | Every assignment/rubric item mapped to evidence |
| `docs/test_report.md` | Verified results and outstanding local checks |

## 1. Install on Windows 11

1. Install 64-bit Python 3.12 from [python.org](https://www.python.org/downloads/windows/). Include the Python launcher (`py`) during installation. Check with `py -3.12 --version` in PowerShell.
2. Use the [official PostgreSQL Windows download page](https://www.postgresql.org/download/windows/). Install a supported PostgreSQL release, including **PostgreSQL Server**, **pgAdmin 4**, and **Command Line Tools**. This project uses standard SQL identity columns supported by PostgreSQL 10 and newer; the actual test server here was 16.2. Record your chosen `postgres` password and port (normally `5432`). Stack Builder add-ons are unnecessary for this project.
3. If pgAdmin was not included, install it from [pgAdmin's Windows download page](https://www.pgadmin.org/download/pgadmin-4-windows/).
4. Extract the project ZIP to a normal folder, for example `C:\Users\YourName\Documents\postgresql-student-management`. Work in the extracted folder containing this README, not inside the ZIP. If Windows displays an extra outer folder, open the inner project folder.


## 2. Create and initialize the database in pgAdmin

1. Open **pgAdmin 4**. Expand **Servers** and connect to your local PostgreSQL server with your PostgreSQL password. If no server is registered, right-click **Servers → Register → Server**. Give it a name such as `Local PostgreSQL`; on **Connection** set Host `127.0.0.1`, your port, Maintenance database `postgres`, Username `postgres`, and your local password. Save.
2. Expand your server → **Databases**. Right-click the existing **postgres** database → **Query Tool**. Enable **Auto-commit** in the Query Tool execution options. Open `database/create_database.sql` with **Ctrl+O**, then press **F5** (or **Execute Script**). Run `CREATE DATABASE` by itself, outside a transaction. If `student_management` already exists, skip this step.
3. Right-click **Databases → Refresh**. Select **student_management**, then right-click → **Query Tool**. Confirm the Query Tool's database is **student_management**, not `postgres`.
4. Open `database/init.sql` with **Ctrl+O**. Execute the entire script with **F5**. It creates the table and inserts all three initial rows in one transaction. It deliberately refuses to replace an existing table.
5. Open `database/verify.sql` and press **F5**. In **Data Output** you should see exactly the following rows on a fresh initialization:

| student_id | first_name | last_name | email | enrollment_date |
| --- | --- | --- | --- | --- |
| 1 | John | Doe | john.doe@example.com | 2023-09-01 |
| 2 | Jane | Smith | jane.smith@example.com | 2023-09-01 |
| 3 | Jim | Beam | jim.beam@example.com | 2023-09-02 |

6. Refresh **Schemas → public → Tables** to locate **students**. The table is `public.students`.

**Alternative initialization:** run `schema.sql`, then `seed.sql` instead of `init.sql`. Choose one route. Do not run both routes, and do not run the seed twice. An initialization error inside `BEGIN` may require `ROLLBACK;` in pgAdmin before retrying. Existing data is never automatically dropped.

**Optional command-line initialization:** if you prefer `psql`, these PowerShell commands prompt for your password. Replace the version folder and port with your installed values; omit the first command if the database already exists.

```powershell
& 'C:\Program Files\PostgreSQL\16\bin\psql.exe' -h 127.0.0.1 -p 5432 -U postgres -d postgres -v ON_ERROR_STOP=1 -f .\database\create_database.sql
& 'C:\Program Files\PostgreSQL\16\bin\psql.exe' -h 127.0.0.1 -p 5432 -U postgres -d student_management -v ON_ERROR_STOP=1 -f .\database\init.sql
```

## 3. Install Python dependencies

Open the extracted project folder in File Explorer. Right-click the folder background → **Open in Terminal** (PowerShell). Run these commands from the folder containing `requirements.txt`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Directly using the virtual environment's Python avoids PowerShell activation/execution-policy issues. If Python 3.12 is your only Python and the launcher is missing, use `python -m venv .venv` after checking `python --version`.

## 4. Configure your local connection

Edit `.env` in the project root. Use the same connection values as pgAdmin:

```dotenv
PGHOST=127.0.0.1
PGPORT=5432
PGDATABASE=student_management
PGUSER=postgres
PGPASSWORD='CHANGE_ME'
```

Replace `CHANGE_ME` with your local PostgreSQL password, save and close Notepad. The template contains **no real password**. Keep `.env` private; `.gitignore` excludes it. Do not show it while recording or upload it manually to GitHub. If a password contains an apostrophe, use suitable dotenv quoting (for example double quotes for an apostrophe-only case). `$` is treated literally because dotenv interpolation is disabled.

Existing `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, or `PGPASSWORD` environment variables take precedence over `.env`. If the wrong database is being used, open a fresh terminal or remove the specific stale variable, for example `Remove-Item Env:PGDATABASE -ErrorAction SilentlyContinue`.

## 5. Run the application

```powershell
.\.venv\Scripts\python.exe .\src\main.py
```

| Menu option | Exact function | Behavior / return value |
| --- | --- | --- |
| 1 | `getAllStudents()` | SELECT and print all five fields, ordered by ID; returns row tuples, or `None` on error |
| 2 | `addStudent(first_name, last_name, email, enrollment_date)` | INSERT; prints and returns the generated ID, or `None` on error |
| 3 | `updateStudentEmail(student_id, new_email)` | UPDATE only the selected ID; returns `True` when found, `False` when absent or on error |
| 4 | `deleteStudent(student_id)` | DELETE only the selected ID; returns `True` when deleted, `False` when absent or on error |
| 0 | — | Exit; Ctrl+C or end-of-input also exits cleanly |

For option 2, enter `Alex`, `Chen`, `alex.chen@example.com`, and `2024-01-15` when prompted. Note the actual `student_id` printed by the application. Use that ID for options 3 and 4; do not assume it is always 4. For option 3 use `alex.chen.updated@example.com`. After each change, switch to pgAdmin and execute `verify.sql` again. The expected row counts are **3 → 4 → 4 → 3**.

Blank enrollment date becomes SQL `NULL`, as allowed by the schema. Names and email cannot be blank in the application. Email is stored as text with a UNIQUE constraint; the assignment does not require email syntax validation. Dates must be valid `YYYY-MM-DD`; IDs must be positive PostgreSQL integers. Missing IDs and duplicate emails produce clear messages, and the menu remains usable.

## Schema and connection design

| Field | PostgreSQL definition | Meaning |
| --- | --- | --- |
| student_id | `INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` | Automatic integer ID; primary key prevents duplicates and NULL |
| first_name | `TEXT NOT NULL` | Required first name |
| last_name | `TEXT NOT NULL` | Required last name |
| email | `TEXT NOT NULL UNIQUE` | Required, unique email value |
| enrollment_date | `DATE` | Optional date |

`IDENTITY` implements PostgreSQL auto-increment; literal `AUTO_INCREMENT` is not PostgreSQL syntax. Each function opens a new connection and cursor. Psycopg 3 connection context managers commit on success, roll back on exceptions, and close the connection. Success is printed after the context exits. User values are passed separately through `%s` placeholders, preventing them from becoming SQL code. No simulated records or cached database results are used. Gaps in generated IDs after failed inserts or deletions are normal.

## 6. Verify locally

Run from the project root after setting `.env` and creating the database:

```powershell
.\.venv\Scripts\python.exe .\tests\integration_test.py
```

The suite opens the configured database for administration, creates a uniquely named **temporary test database**, initializes and tests that database, then drops it. It does **not** reset or modify `student_management.students`. Your PostgreSQL role needs **CREATEDB** privilege; the default local `postgres` account has it. A successful run ends with `Ran 15 tests` and `OK`. If interrupted before cleanup, an unused `student_crud_test_...` database may remain; it can be removed in pgAdmin after confirming its name. Do not record the automated tests as a replacement for showing the four application functions.

Then perform the manual Windows/pgAdmin checks in [docs/demonstration_checklist.md](docs/demonstration_checklist.md). See [docs/test_report.md](docs/test_report.md) for the actual test scope; Windows and your installed pgAdmin were not run here.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `py` is not recognized | Install Python with the launcher or use your installed `python` command after checking its version |
| `No module named psycopg` / `dotenv` | Install requirements with `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`; run using that same Python |
| `database connection failed` | Check Windows **Services** (`services.msc`): PostgreSQL must be running. Match pgAdmin's host, port, user, database and password in `.env` |
| `Replace CHANGE_ME` | Edit and save `.env`; do not edit only `.env.example` |
| `students table not found` | Connect pgAdmin to `student_management` and run `init.sql`; check `PGDATABASE` |
| `database ... does not exist` in pgAdmin | Run `create_database.sql` against `postgres`, then open a new Query Tool for the new database |
| `CREATE DATABASE cannot run inside a transaction block` | Enable Auto-commit; run `ROLLBACK;` if needed, then execute `create_database.sql` alone |
| `relation students already exists` | Do not initialize twice. Inspect existing data with `verify.sql`. If a disposable rehearsal reset is wanted, read and run `reset_demo.sql` |
| `current transaction is aborted` | In the affected pgAdmin Query Tool run `ROLLBACK;`, correct the original error, then retry |
| Email already in use | Use a different email or delete only your previous demonstration row |
| New row has an ID greater than 4 | Normal sequence behavior. Use the actual ID printed by option 2 |
| pgAdmin still shows old rows | Re-run the SELECT with F5; keep Auto-commit enabled. Python and pgAdmin must connect to the same database and server |
| Tests report `permission denied to create database` | Run tests with your local `postgres` role, or manually verify the app with pgAdmin; ordinary CRUD only needs table/sequence privileges |
| Terminal text too small | Enlarge the terminal font (Ctrl+mouse wheel) before recording |


Optional Git commands after installing Git and creating the empty public repository (replace `YOUR_GITHUB_USERNAME` before running):

```powershell
git init
git branch -M main
git add README.md requirements.txt .gitignore .env.example database src docs tests
git status
git commit -m "Implement PostgreSQL student CRUD application"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/postgresql-student-management.git
git push -u origin main
```

Inspect `git status` before committing; `.env` must not appear. Git may ask you to configure your own commit name/email or sign in. Do not use your PostgreSQL password as a GitHub credential.

