const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const crypto = require('crypto-js');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

const PORT = process.env.PORT || 5000;
const JWT_SECRET = process.env.JWT_SECRET || 'super-secret-key';
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || 'encryption-key-123';

// Mock DB
const users = [];

// Auth Middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// Routes
app.post('/api/signup', async (req, res) => {
  const { email, password, name } = req.body;
  if (users.find(u => u.email === email)) return res.status(400).json({ message: 'User exists' });

  const hashedPassword = await bcrypt.hash(password, 10);
  const newUser = { id: Date.now(), email, password: hashedPassword, name, profile: null };
  users.push(newUser);
  res.status(201).json({ message: 'User created' });
});

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }

  const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: '1h' });
  res.json({ token, user: { name: user.name, email: user.email } });
});

// Store Encrypted Wearable Data
app.post('/api/profile/sync', authenticateToken, (req, res) => {
  const { wearableData } = req.body;
  const userIndex = users.findIndex(u => u.id === req.user.id);
  
  // Encrypt the sensitive health data
  const encryptedData = crypto.AES.encrypt(JSON.stringify(wearableData), ENCRYPTION_KEY).toString();
  users[userIndex].profile = encryptedData;
  
  res.json({ message: 'Profile synced and encrypted', status: 'success' });
});

app.get('/api/profile', authenticateToken, (req, res) => {
  const user = users.find(u => u.id === req.user.id);
  if (!user || !user.profile) return res.status(404).json({ message: 'No profile' });

  const bytes = crypto.AES.decrypt(user.profile, ENCRYPTION_KEY);
  const decryptedData = JSON.parse(bytes.toString(crypto.enc.Utf8));
  res.json(decryptedData);
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
