// const express = require('express')
// const cors = require('cors')
// const bodyParser = require('body-parser')
// const mysql = require('mysql2')

// const app = express()
// const PORT = 3000

// app.use(cors())
// app.use(bodyParser.json())

// // 数据库连接
// const db = mysql.createConnection({
//   host: 'localhost',
//   user: 'root',       
//   password: '123456', 
//   database: 'target_tracker'
// })

// db.connect(err => {
//   if(err){
//     console.error('❌ 数据库连接失败:', err)
//     process.exit(1)
//   }
//   console.log('✅ 数据库连接成功')
// })
//   const createTableSQL = `
//     CREATE TABLE IF NOT EXISTS users (
//       id INT AUTO_INCREMENT PRIMARY KEY,
//       username VARCHAR(50) NOT NULL UNIQUE,
//       password VARCHAR(255) NOT NULL,
//       role ENUM('admin','user') NOT NULL DEFAULT 'user'
//     );
//   `
//   db.query(createTableSQL, (err) => {
//     if (err) console.error('创建 users 表失败: ', err)
//     else console.log('✅ users 表已准备好')
//   })

// // 登录接口
// app.post('/api/login', (req,res)=>{
//   const { username, password } = req.body
//   db.query('SELECT * FROM users WHERE username=? AND password=?', [username,password], (err,results)=>{
//     if(err) return res.status(500).json({message:'数据库查询错误'})
//     if(results.length===0) return res.status(401).json({message:'账号或密码错误'})
//     res.json({message:'登录成功', user:results[0]})
//   })
// })

// // 注册接口（默认普通用户）
// app.post('/api/register', (req,res)=>{
//   const { username, password } = req.body
//   db.query('INSERT INTO users(username,password,role) VALUES(?,?,?)', [username,password,'user'], (err)=>{
//     if(err) return res.status(500).json({message:'注册失败或用户名已存在'})
//     res.json({message:'注册成功'})
//   })
// })

// // 获取用户列表（管理员）
// app.get('/api/users', (req,res)=>{
//   db.query('SELECT id,username,role,password FROM users', (err,results)=>{
//     if(err) return res.status(500).json({message:'查询失败'})
//     res.json(results)
//   })
// })

// // 修改密码（管理员或用户自己）
// app.put('/api/users/:id/password', (req,res)=>{
//   const { id } = req.params
//   const { password } = req.body
//   db.query('UPDATE users SET password=? WHERE id=?', [password,id], (err)=>{
//     if(err) return res.status(500).json({message:'修改失败'})
//     res.json({message:'修改成功'})
//   })
// })

// // 删除用户（管理员）
// app.delete('/api/users/:id', (req,res)=>{
//   const { id } = req.params
//   db.query('DELETE FROM users WHERE id=?', [id], (err)=>{
//     if(err) return res.status(500).json({message:'删除失败'})
//     res.json({message:'删除成功'})
//   })
// })

// app.listen(PORT, ()=>{
//   console.log(`🚀 后端服务已启动: http://localhost:${PORT}`)
// })
// serve.js
const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const mysql = require('mysql2')
const multer = require('multer')
const path = require('path')

const app = express()
const PORT = 3000

app.use(cors())
app.use(bodyParser.json())
app.use('/uploads', express.static(path.join(__dirname, 'uploads'))) // 静态文件访问

// 数据库连接
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'target_tracker'
})

db.connect(err => {
  if(err){
    console.error('❌ 数据库连接失败:', err)
    process.exit(1)
  }
  console.log('✅ 数据库连接成功')
})

// 创建表（启动自动创建）
const createTableSQL = `
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role ENUM('admin','user') NOT NULL DEFAULT 'user',
  email VARCHAR(100),
  coins INT DEFAULT 0,
  avatar VARCHAR(255)
);
`
db.query(createTableSQL, (err)=>{
  if(err) console.error('创建 users 表失败:', err)
  else console.log('✅ users 表已准备好')
})

// 登录
app.post('/api/login', (req,res)=>{
  const { username, password } = req.body
  db.query('SELECT * FROM users WHERE username=? AND password=?', [username,password], (err,results)=>{
    if(err) return res.status(500).json({message:'数据库查询错误'})
    if(results.length===0) return res.status(401).json({message:'账号或密码错误'})
    res.json({message:'登录成功', user:results[0]})
  })
})

// 注册
app.post('/api/register', (req,res)=>{
  const { username, password, email } = req.body
  db.query('INSERT INTO users(username,password,role,email) VALUES(?,?,?,?)', 
    [username,password,'user', email], (err)=>{
      if(err) return res.status(500).json({message:'注册失败或用户名已存在'})
      res.json({message:'注册成功'})
    })
})
// 获取用户列表（管理员）
app.get('/api/users', (req,res)=>{
  db.query('SELECT id,username,role,password,email FROM users', (err,results)=>{
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
// 修改邮箱（管理员或用户自己）
app.put('/api/users/:id/email', (req,res)=>{
  const { id } = req.params
  const { email } = req.body
  db.query('UPDATE users SET email=? WHERE id=?', [email,id], (err)=>{
    if(err) return res.status(500).json({message:'修改失败'})
    res.json({message:'修改成功'})
  })
})

// 删除用户（管理员）
app.delete('/api/users/:id', (req, res) => {
  const { id } = req.params

  // 先查出被删除的用户，确认不是自己
  db.query('SELECT * FROM users WHERE id=?', [id], (err, results) => {
    if (err) return res.status(500).json({ message: '查询用户失败' })
    if (results.length === 0) return res.status(404).json({ message: '用户不存在' })

    const user = results[0]

    // ⚠️ 这里直接判断：如果是管理员账号就拒绝删除
    if (user.role === 'admin') {
      return res.status(400).json({ message: '不能删除管理员账号！' })
    }

    // 不是管理员才允许删除
    db.query('DELETE FROM users WHERE id=?', [id], (err) => {
      if (err) return res.status(500).json({ message: '删除失败' })
      res.json({ message: '删除成功' })
    })
  })
})



app.get('/api/personal/:id', (req,res)=>{
  const { id } = req.params
  db.query('SELECT id, username, email, coins, avatar FROM users WHERE id=?', [id], (err,results)=>{
    if(err) return res.status(500).json({message:'查询失败'})
    if(results.length===0) return res.status(404).json({message:'用户不存在'})
    res.json(results[0])
  })
})

// 上传头像
const storage = multer.diskStorage({
  destination: (req,file,cb)=> cb(null, 'uploads/'),
  filename: (req,file,cb)=> cb(null, Date.now() + path.extname(file.originalname))
})
const upload = multer({ storage })
app.post('/api/personal/:id/avatar', upload.single('avatar'), (req,res)=>{
  const { id } = req.params
  const avatarPath = `/uploads/${req.file.filename}`
  db.query('UPDATE users SET avatar=? WHERE id=?', [avatarPath,id], (err)=>{
    if(err) return res.status(500).json({message:'更新头像失败'})
    res.json({message:'头像更新成功', avatar: avatarPath})
  })
})

// 充值金币
app.post('/api/personal/:id/recharge', (req,res)=>{
  const { id } = req.params
  const { coins } = req.body
  db.query('UPDATE users SET coins = coins + ? WHERE id=?', [coins,id], (err)=>{
    if(err) return res.status(500).json({message:'充值失败'})
    res.json({message:'充值成功'})
  })
})
app.post('/api/track/target', (req, res) => {
  const { userId, targetId } = req.body
  const user = users[userId]
  if (!user) return res.status(404).json({ success: false, message: '用户不存在' })

  if (user.coins < 100) {
    return res.json({ success: false, message: '金币不足，无法追踪' })
  }

  // 扣除金币
  user.coins -= 100

  // 这里可以记录追踪任务，比如存数据库
  console.log(`用户 ${user.username} 追踪目标 ${targetId}，金币剩余 ${user.coins}`)

  res.json({
    success: true,
    message: `追踪成功，扣除 100 金币，剩余 ${user.coins}`,
    newBalance: user.coins
  })
})
app.listen(PORT, ()=> console.log(`🚀 服务启动: http://localhost:${PORT}`))
