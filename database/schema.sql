-- Run in student_management. This intentionally fails if students already exists.
-- IDENTITY generates an INTEGER automatically; PRIMARY KEY adds uniqueness
-- and NOT NULL. No extra constraints are imposed on the optional date.
CREATE TABLE public.students (
    student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

