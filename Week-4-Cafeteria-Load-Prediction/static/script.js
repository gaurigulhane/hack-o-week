const actualLoadEl = document.getElementById('actual-load');
const predictedLoadEl = document.getElementById('predicted-load');
const tempEl = document.getElementById('temp');
const humidityEl = document.getElementById('humidity');
const insightTextEl = document.getElementById('insight-text');

const ctx = document.getElementById('loadChart').getContext('2d');

let chartData = {
    labels: [],
    datasets: [
        {
            label: 'Actual Load',
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            data: [],
            fill: true,
            tension: 0.4
        },
        {
            label: 'Predicted Load',
            borderColor: '#f472b6',
            backgroundColor: 'transparent',
            data: [],
            fill: false,
            borderDash: [5, 5],
            tension: 0.4
        }
    ]
};

const chart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            x: {
                display: true,
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            },
            y: {
                display: true,
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#94a3b8' },
                beginAtZero: true
            }
        },
        animation: { duration: 0 } // Smoother real-time updates
    }
});

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

    ws.onopen = () => {
        console.log('Connected to WebSocket');
        insightTextEl.innerText = "Connection established. Receiving live predictions...";
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Update UI stats
        actualLoadEl.innerText = data.actual_load;
        predictedLoadEl.innerText = data.predicted_load;
        tempEl.innerText = data.temperature + '°C';
        humidityEl.innerText = data.humidity + '%';

        // Dynamic Insights
        const diff = data.actual_load - data.predicted_load;
        if (Math.abs(diff) < 5) {
            insightTextEl.innerText = "Stabilized flow. Predictions are accurately tracking actual cafeteria load.";
        } else if (diff > 5) {
            insightTextEl.innerText = "Surge alert! Actual load is higher than predicted. Lunch-hour rush peaking.";
        } else {
            insightTextEl.innerText = "Load easing. Current occupancy is below predicted levels.";
        }

        // Update Chart
        const maxPoints = 20;
        if (chartData.labels.length >= maxPoints) {
            chartData.labels.shift();
            chartData.datasets[0].data.shift();
            chartData.datasets[1].data.shift();
        }

        chartData.labels.push(data.time);
        chartData.datasets[0].data.push(data.actual_load);
        chartData.datasets[1].data.push(data.predicted_load);

        chart.update();
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected. Retrying in 5 seconds...');
        insightTextEl.innerText = "Connection lost. Reconnecting...";
        setTimeout(connectWebSocket, 5000);
    };
}

connectWebSocket();
