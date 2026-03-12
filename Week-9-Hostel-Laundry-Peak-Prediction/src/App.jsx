import React, { useState, useMemo } from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell
} from 'recharts';
import { Clock, Users, Zap, Calendar, Info, TrendingDown, TrendingUp } from 'lucide-react';
import { generateLaundryHistory, classifyState } from './utils/laundryData';
import { format } from 'date-fns';

const App = () => {
  const [history] = useState(generateLaundryHistory());
  const [whatIfHour, setWhatIfHour] = useState(new Date().getHours());
  const [scenarioBoost, setScenarioBoost] = useState(0);

  const currentDay = new Date().getDay();
  
  // Forecast logic: simplified trend + periodicity
  const forecastData = useMemo(() => {
    const next24Hours = [];
    const now = new Date();
    for (let i = 0; i < 24; i++) {
      const h = (now.getHours() + i) % 24;
      const d = (now.getDay() + (now.getHours() + i >= 24 ? 1 : 0)) % 7;
      
      // Predict based on history for this hour/day
      const similarPoints = history.filter(p => p.hour === h && p.day === d);
      const avgUsage = similarPoints.length > 0 
        ? similarPoints.reduce((acc, curr) => acc + curr.usage, 0) / similarPoints.length 
        : 30;
      
      next24Hours.push({
        time: `${h}:00`,
        usage: Math.round(avgUsage),
        category: classifyState(history, h, d)
      });
    }
    return next24Hours;
  }, [history]);

  const projectedUsage = useMemo(() => {
    const base = forecastData.find(f => f.time === `${whatIfHour}:00`)?.usage || 0;
    return Math.min(100, base + scenarioBoost);
  }, [whatIfHour, scenarioBoost, forecastData]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass" style={{ padding: '0.5rem 1rem', background: 'rgba(15, 23, 42, 0.9)' }}>
          <p style={{ fontWeight: 'bold' }}>{label}</p>
          <p style={{ color: 'var(--primary)' }}>Usage: {payload[0].value}%</p>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Status: {payload[0].payload.category}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="container">
      <div className="header">
        <div className="title-group">
          <span className="badge" style={{ background: 'rgba(139, 92, 246, 0.2)', color: '#a78bfa', marginBottom: '0.5rem', display: 'inline-block' }}>
            Week 9 • Hostel Analytics
          </span>
          <h1>Laundry Peak Prediction</h1>
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Current Status</p>
          <span className="badge" style={{ 
            background: projectedUsage > 70 ? 'var(--busy)' : projectedUsage > 30 ? 'var(--normal)' : 'var(--quiet)',
            color: 'white'
          }}>
            {projectedUsage > 70 ? 'High Demand' : projectedUsage > 30 ? 'Optimal' : 'Available'}
          </span>
        </div>
      </div>

      <div className="grid">
        <div className="glass border-glow">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <TrendingUp size={20} color="var(--primary)" />
            <h2>Next 24h Forecast</h2>
          </div>
          <div style={{ height: '300px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={forecastData}>
                <defs>
                  <linearGradient id="colorUsage" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="time" stroke="#475569" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#475569" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="usage" stroke="var(--primary)" fillOpacity={1} fill="url(#colorUsage)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <Zap size={20} color="var(--accent)" />
            <h2>What-If Simulator</h2>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '2rem' }}>
            Adjust the slider to simulate traffic changes and see real-time machine availability predictions.
          </p>
          
          <div className="slider-container">
            <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
              <span>Time: {whatIfHour}:00</span>
              <span>Extra Load: +{scenarioBoost}%</span>
            </div>
            <input 
              type="range" min="0" max="23" value={whatIfHour} 
              onChange={(e) => setWhatIfHour(parseInt(e.target.value))} 
            />
            <input 
              type="range" min="0" max="50" value={scenarioBoost} 
              onChange={(e) => setScenarioBoost(parseInt(e.target.value))} 
            />
          </div>

          <div style={{ marginTop: '2rem', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: 'var(--text-main)' }}>
              {projectedUsage}%
            </div>
            <p style={{ color: 'var(--text-muted)' }}>Projected Occupancy</p>
          </div>
        </div>
      </div>

      <div className="grid" style={{ marginTop: '1.5rem' }}>
        <div className="glass" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '1rem', borderRadius: '1rem' }}>
            <Info color="var(--primary)" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', marginBottom: '0.25rem' }}>Naive Bayes Model</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Analyzing historical probability for time/day categorization.</p>
          </div>
        </div>
        <div className="glass" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '1rem', borderRadius: '1rem' }}>
            <Calendar color="var(--accent)" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', marginBottom: '0.25rem' }}>Weekend Peak Expected</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>History indicates 40% higher usage on Sundays.</p>
          </div>
        </div>
      </div>

      <footer style={{ marginTop: '4rem', textAlign: 'center', paddingBottom: '2rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
        Hostel Laundry Hub • Smart Campus Initiatives 2026
      </footer>
    </div>
  );
};

export default App;
