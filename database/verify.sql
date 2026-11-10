-- Re-run this SELECT in pgAdmin after EACH application operation.
-- Leave Auto-commit enabled so the next SELECT sees committed Python changes.
SELECT student_id, first_name, last_name, email, enrollment_date
FROM public.students
ORDER BY student_id;

