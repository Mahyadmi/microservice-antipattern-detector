-- Create sonarqube database for SonarQube
CREATE DATABASE sonarqube;
GRANT ALL PRIVILEGES ON DATABASE sonarqube TO antipattern_user;

-- Ensure main database exists
\c antipattern_db;

-- Create any initial tables if needed
CREATE TABLE IF NOT EXISTS health_check (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
