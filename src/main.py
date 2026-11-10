"""A small PostgreSQL student CRUD application with an interactive CLI.

The assignment's camelCase function names and parameter lists are preserved.
Each operation uses a real PostgreSQL connection, transaction and SQL statement.
"""

import os
from datetime import date
from pathlib import Path

import psycopg
from dotenv import load_dotenv


# Resolve .env relative to this file, so launching from another folder also works.
# Existing environment variables take priority. Disable interpolation so a dollar
# sign in a password is treated literally. No credentials are printed or logged.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env", override=False, interpolate=False)


def get_connection():
    """Open one connection using local configuration; the caller closes it."""
    try:
        port = int(os.getenv("PGPORT", "5432"))
    except ValueError:
        raise ValueError("PGPORT must be a number in .env.") from None
    if not 1 <= port <= 65535:
        raise ValueError("PGPORT must be between 1 and 65535.")
    if os.getenv("PGPASSWORD") == "CHANGE_ME":
        raise ValueError("Replace CHANGE_ME with your local password in .env.")
    return psycopg.connect(
        host=os.getenv("PGHOST", "127.0.0.1"),
        port=port,
        dbname=os.getenv("PGDATABASE", "student_management"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        connect_timeout=5,
    )


def required_text(value, field):
    """Reject missing/blank CLI values before sending them to the database."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required and cannot be blank.")
    return value.strip()


def parse_student_id(value):
    """Accept a positive integer ID or its text representation from input()."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("Student ID must be a positive integer.")
    try:
        student_id = int(value)
    except ValueError:
        raise ValueError("Student ID must be a positive integer.") from None
    if not 1 <= student_id <= 2147483647:
        raise ValueError("Student ID must be between 1 and 2147483647.")
    return student_id


def parse_enrollment_date(value):
    """Allow a date, an ISO date string, or None/blank for the nullable column."""
    if value is None or value == "":
        return None
    if type(value) is date:
        return value
    if isinstance(value, str):
        try:
            parsed = date.fromisoformat(value)
            if parsed.isoformat() == value:
                return parsed
        except ValueError:
            pass
    raise ValueError("Enrollment date must be YYYY-MM-DD, or blank for NULL.")


def report_error(error):
    """Explain common failures without exposing connection strings/passwords."""
    if isinstance(error, psycopg.errors.UniqueViolation):
        print("Error: that email is already in use. No changes were saved.")
    elif isinstance(error, psycopg.errors.NotNullViolation):
        print("Error: a required database field is missing. No changes were saved.")
    elif isinstance(error, psycopg.errors.UndefinedTable):
        print("Error: students table not found. Run database/init.sql in the correct database.")
    elif isinstance(error, psycopg.OperationalError):
        print("Error: database connection failed. Check the PostgreSQL service and .env settings.")
    elif isinstance(error, (ValueError, TypeError)):
        print(f"Input/configuration error: {error}")
    else:
        print("Error: the database operation failed. No changes were saved. Check the schema and permissions.")


def getAllStudents():
    """SELECT and display every student; return rows, or None on failure."""
    try:
        # Psycopg 3 commits on a normal exit, rolls back on an exception, and
        # closes the connection. The nested cursor context also closes itself.
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT student_id, first_name, last_name, email, enrollment_date "
                    "FROM public.students ORDER BY student_id"
                )
                students = cursor.fetchall()
        # Report success only after the transaction context exits successfully.
        if not students:
            print("No students found. Total students: 0")
        else:
            print("student_id | first_name | last_name | email | enrollment_date")
            for student in students:
                print(" | ".join("NULL" if value is None else str(value) for value in student))
            print(f"Total students: {len(students)}")
        return students
    except (psycopg.Error, ValueError, TypeError) as error:
        report_error(error)
        return None


def addStudent(first_name, last_name, email, enrollment_date):
    """INSERT one student; return the generated ID, or None on failure."""
    try:
        first_name = required_text(first_name, "First name")
        last_name = required_text(last_name, "Last name")
        email = required_text(email, "Email")
        enrollment_date = parse_enrollment_date(enrollment_date)
        with get_connection() as connection:
            with connection.cursor() as cursor:
                # Pass values separately: never concatenate user input into SQL.
                cursor.execute(
                    "INSERT INTO public.students (first_name, last_name, email, enrollment_date) "
                    "VALUES (%s, %s, %s, %s) RETURNING student_id",
                    (first_name, last_name, email, enrollment_date),
                )
                student_id = cursor.fetchone()[0]
        print(f"Student added successfully. student_id={student_id}")
        return student_id
    except (psycopg.Error, ValueError, TypeError) as error:
        report_error(error)
        return None


def updateStudentEmail(student_id, new_email):
    """UPDATE only the chosen ID; return True if changed, otherwise False."""
    try:
        student_id = parse_student_id(student_id)
        new_email = required_text(new_email, "Email")
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE public.students SET email = %s WHERE student_id = %s "
                    "RETURNING student_id",
                    (new_email, student_id),
                )
                updated = cursor.fetchone()
        if updated is None:
            print(f"No student found with student_id={student_id}. No changes made.")
            return False
        print(f"Email updated successfully for student_id={student_id}.")
        return True
    except (psycopg.Error, ValueError, TypeError) as error:
        report_error(error)
        return False


def deleteStudent(student_id):
    """DELETE only the chosen ID; return True if removed, otherwise False."""
    try:
        student_id = parse_student_id(student_id)
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM public.students WHERE student_id = %s RETURNING student_id",
                    (student_id,),
                )
                deleted = cursor.fetchone()
        if deleted is None:
            print(f"No student found with student_id={student_id}. No changes made.")
            return False
        print(f"Student deleted successfully. student_id={student_id}")
        return True
    except (psycopg.Error, ValueError, TypeError) as error:
        report_error(error)
        return False


def main():
    """Dispatch menu choices to the four required functions until exit."""
    print("PostgreSQL Student Management")
    while True:
        print("\n1. getAllStudents()")
        print("2. addStudent(first_name, last_name, email, enrollment_date)")
        print("3. updateStudentEmail(student_id, new_email)")
        print("4. deleteStudent(student_id)")
        print("0. Exit")
        try:
            choice = input("Choose an option: ").strip()
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                email = input("Email: ").strip()
                enrollment_date = input("Enrollment date (YYYY-MM-DD, blank for NULL): ").strip()
                addStudent(first_name, last_name, email, enrollment_date)
            elif choice == "3":
                student_id = input("Student ID: ").strip()
                new_email = input("New email: ").strip()
                updateStudentEmail(student_id, new_email)
            elif choice == "4":
                deleteStudent(input("Student ID: ").strip())
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid option. Enter 0, 1, 2, 3, or 4.")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C or closed input ends the program without a traceback.
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()

