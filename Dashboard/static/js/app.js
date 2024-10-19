const THRESHOLDS = {
    lpg: 2761.28,
    smoke: 65529.52,
    alcohol: 367.48,
    flammable_gas: 31.51,
    methane: 3.57,
    co: 65.95
};

const WEIGHTS = {
    co: 0.5,
    smoke: 0.00,
    alcohol: 0.05,
    methane: 0.30,
    lpg: 0.10,
    flammable_gas: 0.25
};

const MAX_SAFE_INDEX = 0.85; // Define a maximum safe value for the safety index
let lastSafetyStatus = "Safe"; // Track last status to prevent recurrence

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            updateGasPlot(data);
            checkAlerts(data);
            updateSafetyIndex(data); // Calculate and display safety index
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateGasPlot(data) {
    const timestamps = data.map(entry => entry.timestamp);

    const traceCO = {
        x: timestamps,
        y: data.map(entry => entry.co),
        name: 'CO',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'orange', width: 2 }
    };

    const traceLPG = {
        x: timestamps,
        y: data.map(entry => entry.lpg),
        name: 'LPG',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'blue', width: 2 }
    };

    const traceSmoke = {
        x: timestamps,
        y: data.map(entry => entry.smoke),
        name: 'Smoke',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'red', width: 2 }
    };

    const traceAlcohol = {
        x: timestamps,
        y: data.map(entry => entry.alcohol),
        name: 'Alcohol',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'green', width: 2 }
    };

    const traceMethane = {
        x: timestamps,
        y: data.map(entry => entry.methane),
        name: 'Methane',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'purple', width: 2 }
    };

    const traceFlammableGas = {
        x: timestamps,
        y: data.map(entry => entry.flammable_gas),
        name: 'Flammable Gas',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'pink', width: 2 }
    };

    const layout = {
        title: 'Gas Levels (ppm)',
        xaxis: { title: 'Timestamp' },
        yaxis: { title: 'Concentration (ppm)' },
        margin: { t: 50 },
        paper_bgcolor: '#121212',
        plot_bgcolor: '#121212',
        font: { color: '#ffffff' }
    };

    Plotly.newPlot('gas-plot', [traceCO, traceLPG, traceSmoke, traceAlcohol, traceMethane, traceFlammableGas], layout);
}

function checkAlerts(data) {
    const alertsDiv = document.getElementById('alerts');
    alertsDiv.innerHTML = ''; // Clear previous alerts
    let alerts = [];

    data.forEach(entry => {
        if (entry.lpg > THRESHOLDS.lpg) {
            alerts.push(createAlert('Warning: High LPG level detected!', 'danger'));
        }
        if (entry.co > THRESHOLDS.co) {
            alerts.push(createAlert('Danger: Potential engine fault due to high CO levels!', 'danger'));
        }
        if (entry.alcohol > THRESHOLDS.alcohol) {
            alerts.push(createAlert('Warning: High alcohol level detected!', 'danger'));
        }
        if (entry.smoke > THRESHOLDS.smoke) {
            alerts.push(createAlert('Warning: High smoke level detected!', 'danger'));
        }
        if (entry.flammable_gas > THRESHOLDS.flammable_gas) {
            alerts.push(createAlert('Warning: High flammable gas level detected!', 'danger'));
        }
        if (entry.methane > THRESHOLDS.methane) {
            alerts.push(createAlert('Warning: High methane level detected!', 'danger'));
        }
    });

    alerts.forEach(alert => alertsDiv.appendChild(alert)); // Append alerts to the alerts div
}

function createAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${type}`;
    alertDiv.textContent = message;
    return alertDiv;
}

function calculateSafetyIndex(concentrations) {
    let safetyScores = 0;

    for (let gas in concentrations) {
        const concentration = concentrations[gas];
        const threshold = THRESHOLDS[gas];
        const weight = WEIGHTS[gas];
        const score = Math.max(0, 1 - (concentration / threshold));
        safetyScores += score * weight;
    }

    return safetyScores;
}

function updateSafetyIndex(data) {
    const latestEntry = data[data.length - 1]; // Get the latest data entry
    const safetyIndex = calculateSafetyIndex(latestEntry);
    const safetyIndicator = document.getElementById('safety-indicator');

    // Determine safety status
    let safetyStatus = "Safe";
    if (latestEntry.smoke > 600000) {
        safetyStatus = "Unsafe"; // Set unsafe status if smoke exceeds 600,000
    } else if (safetyIndex >= MAX_SAFE_INDEX) {
        safetyStatus = "Unsafe";
    }

    // Update the table
    if (safetyStatus !== lastSafetyStatus) { // Check if the status has changed
        safetyIndicator.textContent = safetyStatus;
        lastSafetyStatus = safetyStatus; // Update the last status
    }

    console.log(`Overall Safety Index: ${safetyIndex.toFixed(2)}, Status: ${safetyStatus}`); // For debugging
}

fetchData();
setInterval(fetchData, 10000); // Fetch data every 10 seconds
