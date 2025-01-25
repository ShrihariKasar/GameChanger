CREATE DATABASE gaming_db;

USE gaming_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE game_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    game_name VARCHAR(100),
    play_hours INT,
    play_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
