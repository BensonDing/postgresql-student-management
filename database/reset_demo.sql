-- OPTIONAL REHEARSAL RESET. Run only in your disposable assignment database.
-- WARNING: deletes ALL students and resets IDs, then restores the three seeds.
-- This is never run automatically by the application or the test runner.
BEGIN;
TRUNCATE TABLE public.students RESTART IDENTITY;
INSERT INTO public.students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
COMMIT;

