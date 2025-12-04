// Methodology Page JavaScript

let cleanDataChart = null;
let comparisonChart = null;

// Load data saat halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
    loadMethodologyData();
});

// Load data untuk methodology page
async function loadMethodologyData() {
    try {
        // Load historical data
        const histResponse = await fetch('/api/historical');
        const histResult = await histResponse.json();
        
        // Load predictions
        const predResponse = await fetch('/api/predictions');
        const predResult = await predResponse.json();
        
        if (histResult.success && predResult.success) {
            updateStats(histResult.data, predResult.data);
            createCleanDataChart(histResult.data);
            createComparisonChart(histResult.data, predResult.data);
        }
    } catch (error) {
        console.error('Error loading methodology data:', error);
    }
}

// Update statistics
function updateStats(historical, predictions) {
    // Stats sudah hardcoded di HTML:
    // - Missing Values: 0 hari
    // - Hari Tutup: 10 hari
    // Tidak perlu perhitungan otomatis
}

// Create clean data chart (30 hari terakhir)
function createCleanDataChart(data) {
    const ctx = document.getElementById('cleanDataChart').getContext('2d');
    
    if (cleanDataChart) {
        cleanDataChart.destroy();
    }
    
    // Ambil 30 hari terakhir
    const last30Days = 30;
    const labels = data.dates.slice(-last30Days).map(d => formatDate(d));
    const potong = data.ayam_potong.slice(-last30Days);
    const kampung = data.ayam_kampung.slice(-last30Days);
    const tua = data.ayam_tua.slice(-last30Days);
    
    cleanDataChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Ayam Potong',
                    data: potong,
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
                },
                {
                    label: 'Ayam Kampung',
                    data: kampung,
                    borderColor: '#34d399',
                    backgroundColor: 'rgba(52, 211, 153, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
                },
                {
                    label: 'Ayam Tua',
                    data: tua,
                    borderColor: '#fbbf24',
                    backgroundColor: 'rgba(251, 191, 36, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
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
                        font: { size: 12 },
                        padding: 15
                    }
                },
                title: {
                    display: true,
                    text: 'Data Bersih - 30 Hari Terakhir',
                    color: '#e0e0e0',
                    font: { size: 16, weight: 'bold' }
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
                    ticks: { color: '#888888' },
                    grid: { color: '#2a2a2a', drawBorder: false }
                },
                x: {
                    ticks: {
                        color: '#888888',
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: { color: '#2a2a2a', drawBorder: false }
                }
            }
        }
    });
}

// Create comparison chart (historis + prediksi)
function createComparisonChart(historical, predictions) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    
    if (comparisonChart) {
        comparisonChart.destroy();
    }
    
    // Ambil 30 hari terakhir historis
    const last30Days = 30;
    const histLabels = historical.dates.slice(-last30Days).map(d => formatDate(d));
    const histPotong = historical.ayam_potong.slice(-last30Days);
    const histKampung = historical.ayam_kampung.slice(-last30Days);
    const histTua = historical.ayam_tua.slice(-last30Days);
    
    // Prediksi 7 hari
    const predLabels = predictions.dates.map(d => formatDate(d));
    const predPotong = predictions.ayam_potong;
    const predKampung = predictions.ayam_kampung;
    const predTua = predictions.ayam_tua;
    
    // Gabungkan labels
    const allLabels = [...histLabels, ...predLabels];
    
    // Gabungkan data (historis + null untuk prediksi, dan sebaliknya)
    const potongHist = [...histPotong, ...Array(predPotong.length).fill(null)];
    const potongPred = [...Array(histPotong.length).fill(null), ...predPotong];
    
    const kampungHist = [...histKampung, ...Array(predKampung.length).fill(null)];
    const kampungPred = [...Array(histKampung.length).fill(null), ...predKampung];
    
    const tuaHist = [...histTua, ...Array(predTua.length).fill(null)];
    const tuaPred = [...Array(histTua.length).fill(null), ...predTua];
    
    comparisonChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allLabels,
            datasets: [
                // Historis (solid lines)
                {
                    label: 'Ayam Potong (Historis)',
                    data: potongHist,
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.1)',
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 2
                },
                {
                    label: 'Ayam Kampung (Historis)',
                    data: kampungHist,
                    borderColor: '#34d399',
                    backgroundColor: 'rgba(52, 211, 153, 0.1)',
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 2
                },
                {
                    label: 'Ayam Tua (Historis)',
                    data: tuaHist,
                    borderColor: '#fbbf24',
                    backgroundColor: 'rgba(251, 191, 36, 0.1)',
                    tension: 0.4,
                    fill: false,
                    borderWidth: 2,
                    pointRadius: 2
                },
                // Prediksi (dashed lines)
                {
                    label: 'Ayam Potong (Prediksi)',
                    data: potongPred,
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.2)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2.5,
                    borderDash: [5, 5],
                    pointRadius: 4,
                    pointBackgroundColor: '#60a5fa'
                },
                {
                    label: 'Ayam Kampung (Prediksi)',
                    data: kampungPred,
                    borderColor: '#34d399',
                    backgroundColor: 'rgba(52, 211, 153, 0.2)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2.5,
                    borderDash: [5, 5],
                    pointRadius: 4,
                    pointBackgroundColor: '#34d399'
                },
                {
                    label: 'Ayam Tua (Prediksi)',
                    data: tuaPred,
                    borderColor: '#fbbf24',
                    backgroundColor: 'rgba(251, 191, 36, 0.2)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2.5,
                    borderDash: [5, 5],
                    pointRadius: 4,
                    pointBackgroundColor: '#fbbf24'
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
                        font: { size: 11 },
                        padding: 10
                    }
                },
                title: {
                    display: true,
                    text: 'Perbandingan: Data Historis (30 hari) vs Prediksi (7 hari)',
                    color: '#e0e0e0',
                    font: { size: 16, weight: 'bold' }
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
                    ticks: { color: '#888888' },
                    grid: { color: '#2a2a2a', drawBorder: false }
                },
                x: {
                    ticks: {
                        color: '#888888',
                        maxRotation: 45,
                        minRotation: 45,
                        font: { size: 10 }
                    },
                    grid: { color: '#2a2a2a', drawBorder: false }
                }
            }
        }
    });
}

// Format tanggal ke bahasa Indonesia
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { day: 'numeric', month: 'short' };
    return date.toLocaleDateString('id-ID', options);
}
