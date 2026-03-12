import React, { useState, useEffect, useMemo } from 'react';
import regression from 'regression';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';
import { Lightbulb, Car, AlertTriangle, TrendingUp, Zap } from 'lucide-react';
import { generateParkingData } from './utils/dataGen';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const App = () => {
  const [data, setData] = useState(generateParkingData());
  const [anomaly, setAnomaly] = useState(null);

  // Polynomial Regression (Degree 2)
  const regressionResult = useMemo(() => {
    const points = data.map(d => [d.vehicles, d.lighting]);
    return regression.polynomial(points, { order: 2 });
  }, [data]);

  useEffect(() => {
    // Check for anomalies: if current lighting is significantly higher than regression prediction
    const lastData = data[data.length - 1];
    const prediction = regressionResult.predict(lastData.vehicles)[1];
    if (lastData.lighting > prediction * 1.3) {
      setAnomaly({
        type: 'High Usage',
        message: `Current light usage (${lastData.lighting}%) is 30% higher than predicted for ${lastData.vehicles} vehicles.`,
        time: new Date().toLocaleTimeString()
      });
    } else {
      setAnomaly(null);
    }
  }, [data, regressionResult]);

  const barChartData = {
    labels: data.map(d => `${d.hour}:00`),
    datasets: [
      {
        label: 'Vehicle Count',
        data: data.map(d => d.vehicles),
        backgroundColor: 'rgba(99, 102, 241, 0.5)',
        borderColor: '#6366f1',
        borderWidth: 1,
        yAxisID: 'y',
      },
      {
        label: 'Light Usage (%)',
        data: data.map(d => d.lighting),
        backgroundColor: 'rgba(16, 185, 129, 0.5)',
        borderColor: '#10b981',
        borderWidth: 1,
        yAxisID: 'y1',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: { display: true, text: 'Vehicles', color: '#94a3b8' },
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
        ticks: { color: '#94a3b8' }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        grid: { drawOnChartArea: false },
        title: { display: true, text: 'Light Usage %', color: '#94a3b8' },
        ticks: { color: '#94a3b8' }
      },
      x: {
        ticks: { color: '#94a3b8' },
        grid: { color: 'rgba(255, 255, 255, 0.05)' }
      }
    },
    plugins: {
      legend: {
        labels: { color: '#f8fafc', font: { family: 'Inter' } }
      }
    }
  };

  return (
    <div className="container">
      <header className="title-section">
        <span className="badge badge-primary">Week 8</span>
        <h1>Parking Lot Lighting Forecast</h1>
        <p style={{ color: 'var(--text-muted)' }}>Polynomial Regression-based predictive lighting control system.</p>
      </header>

      <div className="grid">
        <div className="card glass">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '0.75rem', borderRadius: '0.75rem' }}>
              <Car size={24} color="#818cf8" />
            </div>
            <div>
              <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Total Daily Traffic</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {data.reduce((acc, curr) => acc + curr.vehicles, 0).toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        <div className="card glass">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '0.75rem', borderRadius: '0.75rem' }}>
              <Zap size={24} color="#34d399" />
            </div>
            <div>
              <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Avg. Energy Savings</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>24.8%</p>
            </div>
          </div>
        </div>

        <div className="card glass">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '0.75rem', borderRadius: '0.75rem' }}>
              <TrendingUp size={24} color="#818cf8" />
            </div>
            <div>
              <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Regression Model</h3>
              <p style={{ fontSize: '1rem', fontWeight: '500', color: '#34d399' }}>Polynomial (O2)</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card glass" style={{ marginTop: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h2>Vehicle vs. Lighting Trends</h2>
          <button className="btn btn-primary" onClick={() => setData(generateParkingData())}>Refresh Data</button>
        </div>
        <div className="chart-container">
          <Bar data={barChartData} options={chartOptions} />
        </div>
      </div>

      {anomaly && (
        <div className="card glass" style={{ marginTop: '2rem', border: '1px solid rgba(239, 68, 68, 0.3)', background: 'rgba(239, 68, 68, 0.05)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <AlertTriangle color="#f87171" size={24} />
            <div>
              <h3 style={{ color: '#f87171' }}>System Anomaly Detected</h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{anomaly.message} at {anomaly.time}</p>
            </div>
          </div>
        </div>
      )}

      <footer style={{ marginTop: '4rem', textAlign: 'center', paddingBottom: '2rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
        &copy; 2026 Hack-o-week | Parking Lot Sustainability
      </footer>
    </div>
  );
};

export default App;
