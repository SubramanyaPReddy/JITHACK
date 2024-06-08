CREATE DATABASE IF NOT EXISTS app;
USE app;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS mcq_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    language VARCHAR(50),
    correct_count INT,
    total_questions INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS coding_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    language VARCHAR(50),
    problem TEXT,
    solution TEXT,
    score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


