# PostgreSQL Student Management

This project uses Python and PostgreSQL to manage student records through a command-line menu. It supports viewing, adding, updating, and deleting students.

## Demonstration Video

https://youtu.be/0G8yxR6qiOs

## Requirements

* Python 3.12
* PostgreSQL 16 or newer
* pgAdmin 4
* Python packages listed in `requirements.txt`: Psycopg and python-dotenv

Python does not require a separate compilation step.

## Database Setup

1. Download the repository using **Code → Download ZIP** and extract it.
2. Open pgAdmin and connect to your local PostgreSQL server using your PostgreSQL username and password.
3. Right-click the existing `postgres` database and open **Query Tool**. Enable Auto-commit and run `database/create\_database.sql` to create `student\_management`. Skip this step if the database already exists.
4. Refresh the database list. Open a new Query Tool connected to **student\_management** and run the entire `database/init.sql` file. This creates the table and inserts the three initial records. Run it only once.
5. Run `database/verify.sql` to check the records.

Alternatively, run `schema.sql` followed by `seed.sql` instead of `init.sql`. Do not use both initialization methods.

The `students` table has these fields:

|Field|Type and constraints|
|-|-|
|student\_id|INTEGER, automatically generated identity, PRIMARY KEY|
|first\_name|TEXT, NOT NULL|
|last\_name|TEXT, NOT NULL|
|email|TEXT, NOT NULL, UNIQUE|
|enrollment\_date|DATE, may be NULL|

The initial records are:

|First name|Last name|Email|Enrollment date|
|-|-|-|-|
|John|Doe|john.doe@example.com|2023-09-01|
|Jane|Smith|jane.smith@example.com|2023-09-01|
|Jim|Beam|jim.beam@example.com|2023-09-02|

## Install and Run on Windows

Open PowerShell in the project folder containing `README.md` and `requirements.txt`. Run:

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

Create a file named `.env` in that same folder with the following contents:

```dotenv
PGHOST=127.0.0.1
PGPORT=5432
PGDATABASE=student\_management
PGUSER=postgres
PGPASSWORD='CHANGE\_ME'
```

Replace `CHANGE\_ME` with your own PostgreSQL password. Match the host, port, and user to your pgAdmin connection. Save the filename as `.env`, not `.env.txt`. Existing PostgreSQL environment variables take priority over this file.

Keep `.env` and `.venv` on your computer only. Do not upload them or real passwords to GitHub; this repository does not include a `.gitignore` to exclude them automatically.

Start the program:

```powershell
.\\.venv\\Scripts\\python.exe .\\src\\main.py
```

## Using the Program

|Option|Function|What it does|
|-|-|-|
|1|`getAllStudents()`|Retrieves and displays all students, ordered by ID.|
|2|`addStudent(first\_name, last\_name, email, enrollment\_date)`|Adds a student and displays the generated ID.|
|3|`updateStudentEmail(student\_id, new\_email)`|Updates the email for the given student ID.|
|4|`deleteStudent(student\_id)`|Deletes the student with the given ID.|
|0|Exit|Closes the program.|

Follow the prompts after selecting an option. Enter dates as `YYYY-MM-DD`, or leave the date blank for NULL. Names and email cannot be blank. Use the actual generated ID when updating or deleting a student.

For example, add Alex Chen with `alex.chen@example.com` and `2024-01-15`. Update that student's email to `alex.chen.updated@example.com`, then delete the same student. After each change, switch to pgAdmin and re-run `database/verify.sql`. Starting from the initial data, the row counts should be 3, 4, 4, and 3.

The code uses Psycopg to connect to PostgreSQL and parameterized SQL queries to pass input values safely. Successful operations are committed, failed operations are rolled back, and connections are closed. Errors such as duplicate emails, invalid dates, missing IDs, and connection failures produce messages without ending the menu.

## Testing

To run the integration tests:

```powershell
.\\.venv\\Scripts\\python.exe .\\tests\\integration\_test.py
```

The tests create and remove a separate temporary database, so the configured user needs CREATEDB permission. The local `postgres` user normally has this permission. A successful run ends with `Ran 15 tests` and `OK`. The tests do not change the student table in the assignment database.

## Troubleshooting

* **Connection failed:** check that PostgreSQL is running and that `.env` matches your server settings.
* **Module not found:** install `requirements.txt` and run the program using the virtual environment's Python.
* **Table not found:** check the database name and run `init.sql` in `student\_management`.
* **Table already exists:** do not initialize it again; inspect the current records first. If pgAdmin reports an aborted transaction, run `ROLLBACK;` before retrying.
* **Duplicate email:** use a different email address.
* **Old results in pgAdmin:** keep Auto-commit enabled and re-run the SELECT using F5.

`database/reset\_demo.sql` is optional and deletes all current student records before restoring the initial three. Use it only in a disposable assignment database.

