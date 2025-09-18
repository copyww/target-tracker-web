const mysql = require('mysql2/promise');

async function initDB() {
  // 修改成你本地的账号密码
  const connection = await mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'su15060859582'
  });

  try {
    console.log('🚀 正在创建数据库 target_tracker ...');
    await connection.query(`
      CREATE DATABASE IF NOT EXISTS target_tracker
      CHARACTER SET utf8mb4
      COLLATE utf8mb4_general_ci;
    `);

    await connection.query(`USE target_tracker;`);

    console.log('✅ 正在创建数据表 users ...');
    await connection.query(`
      DROP TABLE IF EXISTS users;
    `);

    await connection.query(`
      CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        role ENUM('user', 'admin') DEFAULT 'user'
      );
    `);

    console.log('👤 正在插入初始管理员账号 ...');
    await connection.query(`
      INSERT INTO users (username, password, role)
      VALUES ('admin', '123456', 'admin');
    `);

    console.log('🎉 数据库初始化完成！管理员账号: admin / 123456');
  } catch (err) {
    console.error('❌ 初始化失败:', err);
  } finally {
    await connection.end();
  }
}

initDB();
