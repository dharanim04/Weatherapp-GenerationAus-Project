document.getElementById('weatherForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const cityInput = document.getElementById('cityInput').value;
    // Split by comma for multiple cities
    const cities = cityInput.split(',').map(c => c.trim()).filter(Boolean);
    const resultDiv = document.getElementById('weatherResult');
    resultDiv.textContent = 'Loading...';

    try {
        const response = await fetch('/api/weather', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cities })
        });
        const data = await response.json();
        if (response.ok) {
            resultDiv.innerHTML = data.map(cityData => {
                if (cityData.error) {
                    return `<div><strong>${cityData.city}:</strong> Error - ${cityData.error}</div>`;
                }
                return `<div>
                    <strong>${cityData.city}</strong><br>
                    Temperature: ${cityData.temperature}°C<br>
                    Wind Speed: ${cityData.windspeed} km/h<br>
                    Humidity: ${cityData.humidity !== undefined ? cityData.humidity + '%' : 'N/A'}
                </div>`;
            }).join('<hr>');
            // Optionally, fetch and display search history
            fetchLastFiveHistory();
        } else {
            resultDiv.textContent = data.error || 'Error fetching weather data.';
        }
    } catch (err) {
        resultDiv.textContent = 'Error: ' + err.message;
    }
});
async function fetchLastFiveHistory() {
    const historyDiv = document.getElementById('historyResult');
    if (!historyDiv) return;
    try {
        const resp = await fetch('/api/history/last5');
        const history = await resp.json();
        if (Array.isArray(history) && history.length > 0) {
            historyDiv.innerHTML = '<h3>Last 5 Searches</h3><div class="history-grid">' +
                history.map((entry, idx) => {
                    return entry.results.map(cityData => {
                        if (cityData.error) {
                            return `<div class="history-card error">
                                <strong>${cityData.city}</strong><br>
                                Error: ${cityData.error}
                            </div>`;
                        }
                        return `<div class="history-card">
                            <strong>${cityData.city}</strong><br>
                            <span>🌡️ ${cityData.temperature}°C</span><br>
                            <span>💨 ${cityData.windspeed} km/h</span><br>
                            <span>💧 ${cityData.humidity !== undefined ? cityData.humidity + '%' : 'N/A'}</span>
                        </div>`;
                    }).join('');
                }).join('') + '</div>';
        } else {
            historyDiv.innerHTML = '';
        }
    } catch (e) {
        historyDiv.innerHTML = '';
    }
}

// Call this after each search and on page load
fetchLastFiveHistory();