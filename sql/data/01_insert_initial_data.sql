-- Insert initial roles into Role Table
INSERT INTO "Role" (role_name) VALUES
('Professor'),
('Graduate Student'),
('Undergraduate Student');

-- Insert initial users for testing
INSERT INTO "User" (username, password, role_id, email) VALUES
('prof_john', 'password123', 1, 'john@example.com'),
('grad_student_mary', 'password123', 2, 'mary@example.com'),
('undergrad_jane', 'password123', 3, 'jane@example.com');