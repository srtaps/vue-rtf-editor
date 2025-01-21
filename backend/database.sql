DROP DATABASE IF EXISTS vebprojekat;

CREATE DATABASE IF NOT EXISTS vebprojekat;
USE vebprojekat;

CREATE TABLE IF NOT EXISTS roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL
);

INSERT INTO roles (role_name) VALUES ('Admin');
INSERT INTO roles (role_name) VALUES ('User');

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    full_name VARCHAR(255) AS (CONCAT(first_name, ' ', last_name)) VIRTUAL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    info TEXT,
    professor VARCHAR(100)
);

INSERT INTO courses (course_id, title, info, professor) VALUES 
    (1, 'Introduction to Computer Science', 'Fundamentals of programming and computational thinking', 'Dr. Smith'),
    (2, 'Advanced Mathematics', 'Complex analysis and abstract algebra', 'Dr. Johnson'),
    (3, 'World History', 'Comprehensive study of major historical events', 'Prof. Williams'),
    (4, 'Organic Chemistry', 'Study of organic compounds and reactions', 'Dr. Brown'),
    (5, 'Literature Analysis', 'Critical analysis of classical literature', 'Prof. Davis');

-- Optional: Add an index to email to speed up queries based on email
CREATE INDEX idx_email ON users(email);

-- Setting DELIMITER to allow trigger creation
DELIMITER //

-- Create a trigger to automatically set the default role to 'User' if not specified
CREATE TRIGGER set_default_role BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.role_id IS NULL THEN
        SET NEW.role_id = (SELECT role_id FROM roles WHERE role_name = 'User' LIMIT 1);
    END IF;
END //

-- Reset DELIMITER to the default
DELIMITER ;