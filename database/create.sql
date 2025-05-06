CREATE DATABASE IF NOT EXISTS game_web;
USE game_web;

CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'player') DEFAULT 'player'
)

-- 'admin' - Полный доступ ко всем функциям, управление пользователями, новостями, турнирами.
-- 'organizer' - Создание и управление турнирами, модерирование комментариев в своих турнирах.
-- 'player' - Регистрация в турнирах, участие в матчах, комментирование новостей и турниров.

CREATE TABLE IF NOT EXISTS games (
    id_game INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
)

CREATE TABLE IF NOT EXISTS news (
    id_news INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INT,
    id_game INT
)

ALTER TABLE news ADD COLUMN is_weekly BOOLEAN DEFAULT FALSE;
ALTER TABLE news ADD COLUMN image_path VARCHAR(255);