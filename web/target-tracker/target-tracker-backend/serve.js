const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const mysql = require('mysql2')

const app = express()
const PORT = 3000

app.use(cors())
app.use(bodyParser.json())

// 数据库连接
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',       
  password: 'su15060859582', 
  database: 'target_tracker'
})

db.connect(err => {
  if(err){
    console.error('❌ 数据库连接失败:', err)
    process.exit(1)
  }
  console.log('✅ 数据库连接成功')
})
  const createTableSQL = `
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(50) NOT NULL UNIQUE,
      password VARCHAR(255) NOT NULL,
      role ENUM('admin','user') NOT NULL DEFAULT 'user'
    );
  `
  db.query(createTableSQL, (err) => {
    if (err) console.error('创建 users 表失败: ', err)
    else console.log('✅ users 表已准备好')
  })

// 登录接口
app.post('/api/login', (req,res)=>{
  const { username, password } = req.body
  db.query('SELECT * FROM users WHERE username=? AND password=?', [username,password], (err,results)=>{
    if(err) return res.status(500).json({message:'数据库查询错误'})
    if(results.length===0) return res.status(401).json({message:'账号或密码错误'})
    res.json({message:'登录成功', user:results[0]})
  })
})

// 注册接口（默认普通用户）
app.post('/api/register', (req,res)=>{
  const { username, password } = req.body
  db.query('INSERT INTO users(username,password,role) VALUES(?,?,?)', [username,password,'user'], (err)=>{
    if(err) return res.status(500).json({message:'注册失败或用户名已存在'})
    res.json({message:'注册成功'})
  })
})

// 获取用户列表（管理员）
app.get('/api/users', (req,res)=>{
  db.query('SELECT id,username,role,password FROM users', (err,results)=>{
    if(err) return res.status(500).json({message:'查询失败'})
    res.json(results)
  })
})

// 修改密码（管理员或用户自己）
app.put('/api/users/:id/password', (req,res)=>{
  const { id } = req.params
  const { password } = req.body
  db.query('UPDATE users SET password=? WHERE id=?', [password,id], (err)=>{
    if(err) return res.status(500).json({message:'修改失败'})
    res.json({message:'修改成功'})
  })
})

// 删除用户（管理员）
app.delete('/api/users/:id', (req,res)=>{
  const { id } = req.params
  db.query('DELETE FROM users WHERE id=?', [id], (err)=>{
    if(err) return res.status(500).json({message:'删除失败'})
    res.json({message:'删除成功'})
  })
})

app.listen(PORT, ()=>{
  console.log(`🚀 后端服务已启动: http://localhost:${PORT}`)
})
