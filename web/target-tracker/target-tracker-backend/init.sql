-- 创建数据库
CREATE DATABASE IF NOT EXISTS target_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE target_tracker;

-- 创建用户表
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  role ENUM('user', 'admin') DEFAULT 'user'
);

-- 初始化一个管理员账号
INSERT INTO users (username, password, role)
VALUES ('admin', '123456', 'admin');
