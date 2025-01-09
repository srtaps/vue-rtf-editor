DROP DATABASE IF EXISTS vebprojekat;

CREATE DATABASE IF NOT EXISTS vebprojekat;
USE vebprojekat;

CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    full_name VARCHAR(255) AS (CONCAT(first_name, ' ', last_name)) VIRTUAL
);

-- Optional: Add an index to email to speed up queries based on email
CREATE INDEX idx_email ON Users(email);