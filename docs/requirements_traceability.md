# Assignment requirements and grading evidence

Source: all five supplied assignment screenshots, including application instructions, submission details, rubric and TA instructions. The original assignment takes priority over suggested project structure. No course code, due date, student number, or video URL was invented.

## Schema and starting data

| Authoritative requirement | Implementation / evidence |
| --- | --- |
| PostgreSQL database and `students` table | `create_database.sql`, `init.sql`, pgAdmin setup in README |
| `student_id`: Integer, Primary Key, Auto-increment | `INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY`; exact data type / identity / PK tested |
| `first_name`: Text, Not Null | `TEXT NOT NULL`; database-level NULL rejection tested |
| `last_name`: Text, Not Null | `TEXT NOT NULL`; database-level NULL rejection tested |
| `email`: Text, Not Null, Unique | `TEXT NOT NULL UNIQUE`; duplicate INSERT/UPDATE and NULL rejection tested |
| `enrollment_date`: Date | Nullable `DATE`; valid date insertion and NULL tested |
| John / Doe / john.doe@example.com / 2023-09-01 | Exact value in `init.sql` and `seed.sql`; tested |
| Jane / Smith / jane.smith@example.com / 2023-09-01 | Exact value in `init.sql` and `seed.sql`; tested |
| Jim / Beam / jim.beam@example.com / 2023-09-02 | Exact value in `init.sql` and `seed.sql`; tested |

## Function requirements

| Required exact signature | Real operation | Verification |
| --- | --- | --- |
| `getAllStudents()` | SELECT all five fields; display every record | Integration test + video section 4 |
| `addStudent(first_name, last_name, email, enrollment_date)` | Parameterized INSERT with generated ID returned | Integration test + video section 5 and pgAdmin SELECT |
| `updateStudentEmail(student_id, new_email)` | Parameterized UPDATE with ID-specific WHERE | Integration test + video section 6 and pgAdmin SELECT |
| `deleteStudent(student_id)` | Parameterized DELETE with ID-specific WHERE | Integration test + video section 7 and pgAdmin SELECT |
| Application connects to PostgreSQL for each function | Psycopg 3 connections/cursors; real transactions | Fresh-connection readbacks and actual CLI subprocesses tested |

## Rubric — total 20 marks

These mappings cover the criteria; they do not guarantee a grade. The grader also needs your actual video and accessible repository.

| Criterion | Marks | Where to assess |
| --- | ---: | --- |
| Proper database/table creation to schema | 1.5 | Database scripts, README setup, video section 2 |
| Accurate initial data insertion | 1.5 | Seed SQL, integration initial-values check, video section 3 |
| Primary key, data types, constraints | 2 | Schema definitions, real constraint tests, video section 2 |
| `getAllStudents()` retrieves and displays | 2.5 | `src/main.py`, tests 1/15, video section 4 |
| `addStudent()` inserts | 2.5 | `src/main.py`, tests 3/6/10/13/15, video section 5 |
| `updateStudentEmail()` updates | 2.5 | `src/main.py`, tests 4/7/12/15, video section 6 |
| `deleteStudent()` removes | 2.5 | `src/main.py`, tests 5/12/15, video section 7 |
| Readability, organization, functions, variables, error handling | 2.5 | Small CLI, helper functions, context managers, meaningful errors |
| Comments and clear README/function documentation | 2.5 | Module/function docstrings, SQL/transaction comments, README |

## Documentation, video and submission

| Requirement from screenshots | Package coverage / required next step |
| --- | --- |
| Comments explain each code segment's purpose/function | Docstrings and comments in application, SQL and tests |
| README gives compile/run steps | README explains Python needs no compilation and gives exact Windows commands |
| New **public** GitHub repository | User must publish; complete upload-ready project supplied |
| Commit source, database creation scripts and README | Package includes all; upload instructions preserve directory structure |
| Organized repository | Separate database, src, docs, tests directories |
| Clear, concise video shows provided schema and data | Timed script sections 2–3; must record locally |
| Show execution of every function | Script sections 4–7 use the actual CLI options |
| INSERT, UPDATE, DELETE effects shown in **pgAdmin** | Immediate F5 SELECT checks in sections 5–7 |
| Video at most **5 minutes** | Target 4:30; rehearsal and playback checks explicitly required |
| Upload video to sharing platform/cloud with viewable link | English/Chinese guides and checklist; user must upload |
| Video link inside README | Clearly marked top-of-README placeholder, to replace after recording |
| Submit repository URL through **Brightspace** | README, Chinese guide and checklist state exact deliverable |
| Additional submission notes if needed | Optional, accurate remarks only |
| TA watches video first and uses it as primary grading evidence | Script prioritizes visible database and real CRUD outcomes |
| TA checks source for unclear implementation and comments/README afterward | Readable application and complete setup documentation supplied |
| Late submission: -10% | Included in checklist and guide; check course deadline separately |

