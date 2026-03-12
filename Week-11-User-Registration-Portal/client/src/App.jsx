import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Layout, User, Lock, Mail, RefreshCw, Watch, ShieldCheck, LogOut, CheckCircle2 } from 'lucide-react';

const App = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [syncing, setSyncing] = useState(false);
  const [syncedData, setSyncedData] = useState(null);

  const [formData, setFormData] = useState({ name: '', email: '', password: '' });

  const handleAuth = async (e) => {
    e.preventDefault();
    // Simulate API call for brevity in prototype
    if (!isLogin) {
      // Signup logic mock
      setIsLogin(true);
      alert('Account created! Please login.');
    } else {
      // Login logic mock
      setToken('mock-jwt-token-123');
      setUser({ name: formData.name || 'John Doe', email: formData.email });
    }
  };

  const simulateSync = () => {
    setSyncing(true);
    setTimeout(() => {
      const mockWearable = {
        steps: 8432,
        heartRate: 72,
        sleep: '7h 20m',
        device: 'FitTrack v4.2',
        lastEncryptedSync: new Date().toLocaleTimeString()
      };
      setSyncedData(mockWearable);
      setSyncing(false);
    }, 2000);
  };

  if (!token) {
    return (
      <div className="container">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass auth-card"
        >
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <div style={{ background: 'rgba(244, 114, 182, 0.1)', padding: '1rem', borderRadius: '1rem', display: 'inline-block', marginBottom: '1rem' }}>
              <ShieldCheck size={32} color="var(--primary)" />
            </div>
            <h1>{isLogin ? 'Welcome Back' : 'Create Account'}</h1>
            <p style={{ color: 'var(--text-muted)' }}>Secure Registration Portal</p>
          </div>

          <form onSubmit={handleAuth}>
            {!isLogin && (
              <div className="input-group">
                <label>Full Name</label>
                <input type="text" placeholder="Enter your name" onChange={e => setFormData({...formData, name: e.target.value})} />
              </div>
            )}
            <div className="input-group">
              <label>Email Address</label>
              <input type="email" placeholder="email@example.com" onChange={e => setFormData({...formData, email: e.target.value})} required />
            </div>
            <div className="input-group">
              <label>Password</label>
              <input type="password" placeholder="••••••••" onChange={e => setFormData({...formData, password: e.target.value})} required />
            </div>
            <button type="submit" className="btn btn-primary">
              {isLogin ? 'Sign In' : 'Sign Up'}
            </button>
          </form>

          <p className="auth-toggle">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <span onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? 'Sign Up' : 'Sign In'}
            </span>
          </p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="container" style={{ justifyContent: 'flex-start', paddingTop: '4rem' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div>
          <h1>Hello, {user.name}</h1>
          <p style={{ color: 'var(--text-muted)' }}>Wearable Profile & Encrypted Storage</p>
        </div>
        <button onClick={() => setToken(null)} className="btn" style={{ width: 'auto', background: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)' }}>
          <LogOut size={18} style={{ marginRight: '0.5rem' }} /> Logout
        </button>
      </header>

      <div className="dashboard-grid">
        <div className="glass card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
            <Watch size={24} color="var(--primary)" />
            <h3>Device Status</h3>
          </div>
          <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Model</span>
              <span>{syncedData?.device || 'Not Found'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Sync State</span>
              <span className="status-badge">{syncedData ? 'Encrypted' : 'Standby'}</span>
            </div>
          </div>
          <button onClick={simulateSync} className="btn btn-primary" disabled={syncing}>
            {syncing ? <RefreshCw className="spin" size={18} /> : 'Sync Wearable Data'}
          </button>
        </div>

        <div className="glass card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
            <ShieldCheck size={24} color="var(--accent)" />
            <h3>Security Layer</h3>
          </div>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
            All synced data is encrypted using AES-256 before being stored in the backend vault.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent)', fontSize: '0.875rem' }}>
            <CheckCircle2 size={16} /> JWT Authentication Active
          </div>
        </div>
      </div>

      {syncedData && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass" 
          style={{ marginTop: '2rem' }}
        >
          <h3>Decrypted Profile Preview</h3>
          <div className="dashboard-grid" style={{ marginTop: '1.5rem' }}>
            {[
              { label: 'Total Steps', value: syncedData.steps },
              { label: 'Avg Heart Rate', value: syncedData.heartRate + ' BPM' },
              { label: 'Sleep Quality', value: syncedData.sleep },
              { label: 'Last Encryption', value: syncedData.lastEncryptedSync },
            ].map((item, i) => (
              <div key={i} style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: '0.75rem' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{item.label}</div>
                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', marginTop: '0.25rem' }}>{item.value}</div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      <footer style={{ marginTop: '4rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem', paddingBottom: '2rem' }}>
        Week 11 • Secure User Registration & Health Sync
      </footer>
    </div>
  );
};

export default App;
