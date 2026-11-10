r"""Real PostgreSQL integration tests; no mocked or simulated CRUD results.

Run from the project root: .venv\Scripts\python.exe tests/integration_test.py
Requires CREATEDB privilege (the default local postgres account has it).
Only a uniquely named temporary database is changed; the configured assignment
database is used as an administrative connection and is never initialized/reset.
"""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from uuid import uuid4
from datetime import date

import psycopg
from psycopg import sql

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import main as app  # noqa: E402 - make the standalone application importable


SEEDS = [
    (1, "John", "Doe", "john.doe@example.com", date(2023, 9, 1)),
    (2, "Jane", "Smith", "jane.smith@example.com", date(2023, 9, 1)),
    (3, "Jim", "Beam", "jim.beam@example.com", date(2023, 9, 2)),
]


class PostgreSQLIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Keep the admin connection open for cleanup; never print credentials.
        cls.admin = app.get_connection()
        cls.admin.autocommit = True
        cls.previous_database = os.environ.get("PGDATABASE")
        cls.database = "student_crud_test_" + uuid4().hex[:12]
        cls.admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(cls.database)))
        os.environ["PGDATABASE"] = cls.database
        try:
            with app.get_connection() as connection:
                connection.autocommit = True
                connection.execute((ROOT / "database" / "init.sql").read_text(encoding="utf-8"))
                cls.version = connection.execute("SHOW server_version").fetchone()[0]
            print(f"Real PostgreSQL server version: {cls.version}", flush=True)
        except Exception:
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        # Restore configuration even if DROP DATABASE fails.
        try:
            cls.admin.execute(
                sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(cls.database))
            )
        finally:
            cls.admin.close()
            if cls.previous_database is None:
                os.environ.pop("PGDATABASE", None)
            else:
                os.environ["PGDATABASE"] = cls.previous_database

    def tearDown(self):
        # Every fixture has an ID above the three seeds in this temporary DB.
        with app.get_connection() as connection:
            connection.execute("DELETE FROM public.students WHERE student_id > 3")

    def read_rows(self):
        # A fresh connection proves writes were committed, not merely cached.
        with app.get_connection() as connection:
            return connection.execute("SELECT * FROM public.students ORDER BY student_id").fetchall()

    def call(self, function, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = function(*args)
        return result, output.getvalue()

    def fixture(self):
        student_id, _ = self.call(
            app.addStudent, "Test", "Student", "test.student@example.com", "2024-01-15"
        )
        self.assertIsInstance(student_id, int)
        return student_id

    def test_01_initial_records_and_display(self):
        rows, output = self.call(app.getAllStudents)
        self.assertEqual(rows, SEEDS)
        self.assertIn("student_id | first_name | last_name | email | enrollment_date", output)
        self.assertIn("Total students: 3", output)
        for row in SEEDS:
            self.assertIn(row[3], output)

    def test_02_exact_column_types_and_identity(self):
        with app.get_connection() as connection:
            columns = connection.execute(
                "SELECT column_name, data_type, is_nullable, is_identity "
                "FROM information_schema.columns WHERE table_schema='public' "
                "AND table_name='students' ORDER BY ordinal_position"
            ).fetchall()
        self.assertEqual(columns, [
            ("student_id", "integer", "NO", "YES"),
            ("first_name", "text", "NO", "NO"),
            ("last_name", "text", "NO", "NO"),
            ("email", "text", "NO", "NO"),
            ("enrollment_date", "date", "YES", "NO"),
        ])

    def test_03_add_is_committed_and_auto_incremented(self):
        student_id = self.fixture()
        self.assertGreater(student_id, 3)
        self.assertEqual(self.read_rows(), SEEDS + [
            (student_id, "Test", "Student", "test.student@example.com", date(2024, 1, 15))
        ])

    def test_04_update_only_the_selected_student(self):
        student_id = self.fixture()
        result, output = self.call(app.updateStudentEmail, student_id, "updated@example.com")
        self.assertTrue(result)
        self.assertIn("Email updated successfully", output)
        rows = self.read_rows()
        self.assertEqual(rows[:3], SEEDS)
        self.assertEqual(rows[3], (student_id, "Test", "Student", "updated@example.com", date(2024, 1, 15)))

    def test_05_delete_only_the_selected_student(self):
        student_id = self.fixture()
        result, output = self.call(app.deleteStudent, student_id)
        self.assertTrue(result)
        self.assertIn("Student deleted successfully", output)
        self.assertEqual(self.read_rows(), SEEDS)

    def test_06_duplicate_insert_rolls_back_and_next_call_works(self):
        result, output = self.call(app.addStudent, "Duplicate", "Test", SEEDS[0][3], "2024-01-15")
        self.assertIsNone(result)
        self.assertIn("already in use", output)
        self.assertEqual(self.read_rows(), SEEDS)
        self.fixture()
        self.assertEqual(len(self.read_rows()), 4)

    def test_07_duplicate_update_rolls_back(self):
        student_id = self.fixture()
        before = self.read_rows()
        result, output = self.call(app.updateStudentEmail, student_id, SEEDS[0][3])
        self.assertFalse(result)
        self.assertIn("already in use", output)
        self.assertEqual(self.read_rows(), before)

    def test_08_database_not_null_constraints(self):
        for column in ("first_name", "last_name", "email"):
            with self.subTest(column=column):
                values = {"first_name": "Test", "last_name": "Student", "email": "null.test@example.com"}
                values[column] = None
                with self.assertRaises(psycopg.errors.NotNullViolation):
                    with app.get_connection() as connection:
                        connection.execute(
                            "INSERT INTO public.students (first_name,last_name,email) VALUES (%s,%s,%s)",
                            (values["first_name"], values["last_name"], values["email"]),
                        )
        self.assertEqual(self.read_rows(), SEEDS)

    def test_09_primary_key_duplicate_and_null_are_rejected(self):
        for value, exception in ((1, psycopg.errors.UniqueViolation), (None, psycopg.errors.NotNullViolation)):
            with self.subTest(value=value):
                with self.assertRaises(exception):
                    with app.get_connection() as connection:
                        connection.execute(
                            "INSERT INTO public.students (student_id,first_name,last_name,email) "
                            "OVERRIDING SYSTEM VALUE VALUES (%s,%s,%s,%s)",
                            (value, "Test", "Student", "pk.test@example.com"),
                        )
        self.assertEqual(self.read_rows(), SEEDS)

    def test_10_nullable_enrollment_date(self):
        for index, value in enumerate((None, "")):
            student_id, _ = self.call(app.addStudent, "Optional", "Date", f"date{index}@example.com", value)
            self.assertIsInstance(student_id, int)
        self.assertTrue(all(row[4] is None for row in self.read_rows()[3:]))

    def test_11_invalid_inputs_do_not_write_or_crash(self):
        for value in ("2024-02-30", "bad-date", "20240115"):
            result, output = self.call(app.addStudent, "Test", "Student", "bad@example.com", value)
            self.assertIsNone(result)
            self.assertIn("YYYY-MM-DD", output)
        for values in (("", "Student", "x@example.com"), ("Test", None, "x@example.com"), ("Test", "Student", " ")):
            result, _ = self.call(app.addStudent, *values, "2024-01-15")
            self.assertIsNone(result)
        for value in ("abc", "1.5", 1.5, True, 0, -1, 2147483648):
            self.assertFalse(self.call(app.updateStudentEmail, value, "x@example.com")[0])
            self.assertFalse(self.call(app.deleteStudent, value)[0])
        self.assertEqual(self.read_rows(), SEEDS)

    def test_12_missing_id_is_reported(self):
        for function, args in ((app.updateStudentEmail, (2147483647, "x@example.com")), (app.deleteStudent, (2147483647,))):
            result, output = self.call(function, *args)
            self.assertFalse(result)
            self.assertIn("No student found", output)
        self.assertEqual(self.read_rows(), SEEDS)

    def test_13_parameterized_queries_preserve_literal_input(self):
        name = "Robert'); DROP TABLE public.students; --"
        student_id, _ = self.call(app.addStudent, name, "O'Neil", "literal@example.com", "2024-01-15")
        self.assertIsInstance(student_id, int)
        self.assertEqual(self.read_rows()[3][1:3], (name, "O'Neil"))
        self.assertEqual(self.read_rows()[:3], SEEDS)

    def test_14_connection_and_configuration_errors_are_handled(self):
        # These settings cause REAL connection failures, not mocked SQL results.
        for settings in ({"PGDATABASE": self.database + "_missing"}, {"PGPORT": "1"}):
            with patch.dict(os.environ, settings):
                result, output = self.call(app.getAllStudents)
            self.assertIsNone(result)
            self.assertIn("database connection failed", output)
        with patch.dict(os.environ, {"PGPORT": "invalid"}):
            result, output = self.call(app.getAllStudents)
        self.assertIsNone(result)
        self.assertIn("PGPORT must be a number", output)
        self.assertEqual(self.call(app.getAllStudents)[0], SEEDS)

    def run_cli(self, user_input):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "src" / "main.py")],
            input=user_input, text=True, capture_output=True, timeout=20, cwd=ROOT,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        return completed.stdout

    def test_15_real_interactive_menu_workflow(self):
        output = self.run_cli("9\n1\n2\nCLI\nStudent\ncli.student@example.com\n2024-01-15\n0\n")
        self.assertIn("Invalid option", output)
        self.assertIn("Total students: 3", output)
        self.assertIn("Student added successfully", output)
        student_id = self.read_rows()[3][0]
        output = self.run_cli(f"3\n{student_id}\ncli.updated@example.com\n0\n")
        self.assertIn("Email updated successfully", output)
        self.assertEqual(self.read_rows()[3][3], "cli.updated@example.com")
        output = self.run_cli(f"4\n{student_id}\n1\n0\n")
        self.assertIn("Student deleted successfully", output)
        self.assertIn("Total students: 3", output)
        self.assertEqual(self.read_rows(), SEEDS)
        self.assertIn("Goodbye.", self.run_cli(""))


if __name__ == "__main__":
    unittest.main(verbosity=2)

