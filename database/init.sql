-- Complete table + data initialization for pgAdmin or psql.
-- First create/connect to student_management (see create_database.sql).
-- Run THIS file OR schema.sql followed by seed.sql, never both routes.
-- Existing tables are not dropped. All changes succeed or roll back together.
BEGIN;

CREATE TABLE public.students (
    student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

INSERT INTO public.students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');

COMMIT;

