# Five-minute demonstration: English narration and screen actions

**Target finish: about 4:30. Hard assignment limit: 5:00 for the entire video.**

Read only the **Say** paragraphs. All other text is a stage direction. At an even pace of roughly 100–110 words per minute, speak while clicking/typing and leave short pauses for the result grid. Rehearse once with a stopwatch: timestamps are targets, not a guarantee of your speaking speed. Never skip the three pgAdmin checks to save time.

All results below are **expected results for your successful local run**, not claims that your computer or pgAdmin has already been tested. Use the actual output on your screen.

## Before recording — not spoken

1. Complete the README setup. In pgAdmin, `student_management.public.students` must contain only the three required rows. If necessary, inspect and deliberately run `database/reset_demo.sql` **only in this disposable assignment database**. It deletes all rows and restores the seeds. Never reset a database containing work you need.
2. Prepare two pgAdmin Query Tool tabs connected to `student_management`: tab A opens `database/schema.sql` **for viewing only**, and tab B opens `database/verify.sql`. Keep Auto-commit enabled. Execute tab B once. Do not re-execute tab A during the video.
3. Open PowerShell in the project root. Have the following command ready, but do not run it until section 1:

   ```powershell
   .\.venv\Scripts\python.exe .\src\main.py
   ```

4. Open `src/main.py` in your editor, ready to show `get_connection()` and a CRUD function. Open the README too, ready for the conclusion. Close `.env` and all password dialogs.
5. Use these exact demonstration inputs:

   | Prompt | Input |
   | --- | --- |
   | First name | `Alex` |
   | Last name | `Chen` |
   | Email | `alex.chen@example.com` |
   | Enrollment date | `2024-01-15` |
   | New email | `alex.chen.updated@example.com` |

6. During insertion, write down the actual generated ID. This script calls it **NEW_ID**. On a fresh reset it should be 4, but use the number actually printed. Do **not** type the letters `NEW_ID` into the application. Failed insert attempts and earlier rehearsals can create gaps.
7. Enlarge fonts so all five columns and result rows are readable. Start the screen recorder with microphone audio. Do not record installation, password entry, tests, or the rehearsal reset.

## 1. Introduction — 0:00–0:20

**Show / do:** Show PowerShell in the project folder. Say the paragraph while running the launch command above and letting the numbered menu appear.

**Say:**

> Hello, my name is Benson. This is my PostgreSQL student management application. I used Python with a command-line menu. I will demonstrate the database and all four CRUD functions, including database checks in pgAdmin.

**Expected result:** The terminal shows `PostgreSQL Student Management` and options 1, 2, 3, 4, and 0. Switch to pgAdmin at 0:20.

## 2. Database and schema — 0:20–1:05

**Show / click:** In pgAdmin, show the object explorer path **Servers → your PostgreSQL server → Databases → student_management → Schemas → public → Tables → students**. Refresh **Tables** if needed before recording. Click Query Tool tab A showing `schema.sql`. Point to each definition. **Do not press F5 in this tab.**

**Say:**

> This is the student management database in pgAdmin. I created the students table with five fields. Student ID is an integer primary key. The identity setting generates its value automatically. First name and last name are text fields and cannot be null. Email is also text, cannot be null, and must be unique. Enrollment date uses the date type and can be null. These constraints are enforced by PostgreSQL. I used the initialization script to create the table and load the required data.

**Expected result:** `schema.sql` visibly contains all five exact definitions, including `PRIMARY KEY`, `IDENTITY`, `NOT NULL`, and `UNIQUE`. Switch to tab B in pgAdmin at 1:05.

## 3. Three initial records — 1:05–1:25

**Show / click:** Click tab B (`verify.sql`) and press **F5 / Execute Script**. Show the **Data Output** grid and point to the three rows.

**Say:**

> Here are the three initial students: John Doe, Jane Smith, and Jim Beam. Their email addresses match the assignment. John and Jane enrolled on September first, twenty twenty-three. Jim enrolled on September second. There are exactly three records.

**Expected result:** IDs 1–3; exact emails and dates from the README. Switch to PowerShell at 1:25.

## 4. getAllStudents() — 1:25–1:45

**Show / type:** At `Choose an option:`, enter **1**, then Enter. Keep the output header, all three rows, and count visible.

**Say:**

> I choose option one to run get all students. Python sends a SELECT query to PostgreSQL. The application displays all five fields for every student, ordered by student ID. The total is three, matching pgAdmin.

**Expected result:** The three initial rows and `Total students: 3`. Stay in PowerShell for insertion.

## 5. addStudent() and pgAdmin verification — 1:45–2:30

**Show / type:** Choose **2**. At the four prompts enter, one line at a time:

```text
Alex
Chen
alex.chen@example.com
2024-01-15
```

Read and note the generated numeric ID in `Student added successfully. student_id=...`. Switch to **pgAdmin tab B immediately**, then press **F5** to re-run the SELECT. Point to Alex's row and the email.

**Say:**

> Next, I choose option two to add a student. I enter Alex Chen, an email address, and an enrollment date. The application confirms the insert and shows the new student ID. Now I switch to pgAdmin and run the query again. Alex appears as a fourth record, so the insert was saved in PostgreSQL.

**Expected result:** Four rows: the original three plus Alex Chen, `alex.chen@example.com`, `2024-01-15`, with the actual generated ID. Switch to PowerShell at 2:30.

## 6. updateStudentEmail() and pgAdmin verification — 2:30–3:10

**Show / type:** Choose **3**. Enter the numeric **NEW_ID** noted above at `Student ID:`. At `New email:` enter:

```text
alex.chen.updated@example.com
```

After the success message, switch to **pgAdmin tab B immediately** and press **F5**. Point to Alex's unchanged ID and new email.

**Say:**

> I choose option three to update an email. I use Alex's generated student ID and enter the new email address. The application confirms the update. Back in pgAdmin, I run the query again. Alex now has the updated email. His ID stays the same, and the original three students are unchanged.

**Expected result:** Four rows, with only Alex's email changed to `alex.chen.updated@example.com`. Switch to PowerShell at 3:10.

## 7. deleteStudent() and pgAdmin verification — 3:10–3:45

**Show / type:** Choose **4**. Enter the same numeric **NEW_ID**. After the success message, switch to **pgAdmin tab B immediately** and press **F5**. Pause briefly so the three remaining rows are readable.

**Say:**

> I choose option four and enter Alex's student ID to delete his record. The application confirms the deletion. I check pgAdmin again. Alex is no longer in the table. Only the three original students remain. This shows that the delete affected the correct record.

**Expected result:** Exactly John, Jane, and Jim remain, with their original values. No Alex row. Switch to the code editor at 3:45.

## 8. Python connection and code — 3:45–4:20

**Show / click:** Open the prepared `src/main.py` tab. Show `get_connection()` and then `addStudent()` using the editor's Find command (**Ctrl+F**, search `def addStudent`). Point to `%s`, the values tuple, and `with get_connection()`. Do not open `.env`.

**Say:**

> Python connects to PostgreSQL through Psycopg. Connection settings come from local configuration. Each function opens a connection and executes a real SQL statement. User values are passed separately using placeholders. This prevents input from becoming SQL code. The connection context commits successful operations, rolls back failed operations, and closes the connection. The code also handles duplicate emails, invalid input, and connection errors with clear messages.

**Expected result:** The visible code contains the actual connection call, INSERT with `%s` placeholders, separate values tuple, context managers and error handler. Switch to the README at 4:20.

## 9. Conclusion — 4:20–4:30

**Show / click:** Show the README overview/file list. If time permits, switch to PowerShell and enter **0** to exit. Stop the recorder immediately after speaking.

**Say:**

> The project includes source code, SQL scripts, and setup instructions. All four functions are complete. Thank you.

**Expected result:** A complete recording near 4:30 and **never over 5:00**. Play it back before uploading. The final video link must be added to the README.

