let predictionChart = null;

// Format tanggal ke bahasa Indonesia
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return date.toLocaleDateString('id-ID', options);
}

// Load data prediksi
async function loadPredictions() {
    try {
        const response = await fetch('/api/predictions');
        const result = await response.json();
        
        if (result.success) {
            updateStats(result.data);
            updateChart(result.data);
            updateTable(result.data);
        } else {
            console.error('Gagal memuat prediksi:', result.message);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Update statistik cards
function updateStats(data) {
    const avgPotong = (data.ayam_potong.reduce((a, b) => a + b, 0) / data.ayam_potong.length).toFixed(1);
    const avgKampung = (data.ayam_kampung.reduce((a, b) => a + b, 0) / data.ayam_kampung.length).toFixed(1);
    const avgTua = (data.ayam_tua.reduce((a, b) => a + b, 0) / data.ayam_tua.length).toFixed(1);
    
    document.getElementById('statPotong').textContent = avgPotong;
    document.getElementById('statKampung').textContent = avgKampung;
    document.getElementById('statTua').textContent = avgTua;
}

// Update chart
function updateChart(data) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates.map(d => formatDate(d)),
            datasets: [
                {
                    label: 'Ayam Potong',
                    data: data.ayam_potong,
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#60a5fa',
                    pointBorderColor: '#1e40af',
                    pointBorderWidth: 2
                },
                {
                    label: 'Ayam Kampung',
                    data: data.ayam_kampung,
                    borderColor: '#34d399',
                    backgroundColor: 'rgba(52, 211, 153, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#34d399',
                    pointBorderColor: '#047857',
                    pointBorderWidth: 2
                },
                {
                    label: 'Ayam Tua',
                    data: data.ayam_tua,
                    borderColor: '#fbbf24',
                    backgroundColor: 'rgba(251, 191, 36, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#fbbf24',
                    pointBorderColor: '#b45309',
                    pointBorderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#e0e0e0',
                        font: {
                            size: 12
                        },
                        padding: 15
                    }
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Jumlah (kg)',
                        color: '#a0a0a0'
                    },
                    ticks: {
                        color: '#888888'
                    },
                    grid: {
                        color: '#2a2a2a',
                        drawBorder: false
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Tanggal',
                        color: '#a0a0a0'
                    },
                    ticks: {
                        color: '#888888',
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        color: '#2a2a2a',
                        drawBorder: false
                    }
                }
            }
        }
    });
}

// Update tabel
function updateTable(data) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    
    for (let i = 0; i < data.dates.length; i++) {
        const row = document.createElement('tr');
        const total = data.ayam_potong[i] + data.ayam_kampung[i] + data.ayam_tua[i];
        
        row.innerHTML = `
            <td>${formatDate(data.dates[i])}</td>
            <td>${data.ayam_potong[i].toFixed(1)}</td>
            <td>${data.ayam_kampung[i].toFixed(1)}</td>
            <td>${data.ayam_tua[i].toFixed(1)}</td>
            <td><strong>${total.toFixed(1)}</strong></td>
        `;
        
        tbody.appendChild(row);
    }
}

// Load data saat halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
    loadPredictions();
});
