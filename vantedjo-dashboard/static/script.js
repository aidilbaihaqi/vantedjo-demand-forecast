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
        console.log('🔄 Fetching predictions from API...');
        const response = await fetch('/api/predictions');
        const result = await response.json();
        
        console.log('📦 API Response:', result);
        console.log('✅ Success:', result.success);
        console.log('📊 Data:', result.data);
        
        if (result.success) {
            console.log('🎯 Updating stats...');
            updateStats(result.data);
            console.log('📈 Updating chart...');
            updateChart(result.data);
            console.log('📋 Updating table...');
            updateTable(result.data);
            console.log('✨ All updates complete!');
        } else {
            console.error('❌ Gagal memuat prediksi:', result.message);
            alert('Gagal memuat prediksi: ' + result.message);
        }
    } catch (error) {
        console.error('❌ Error:', error);
        alert('Error loading data: ' + error.message);
    }
}

// Update statistik cards
function updateStats(data) {
    console.log('📊 Calculating averages...');
    console.log('  Ayam Potong data:', data.ayam_potong);
    console.log('  Ayam Kampung data:', data.ayam_kampung);
    console.log('  Ayam Tua data:', data.ayam_tua);
    
    const avgPotong = (data.ayam_potong.reduce((a, b) => a + b, 0) / data.ayam_potong.length).toFixed(1);
    const avgKampung = (data.ayam_kampung.reduce((a, b) => a + b, 0) / data.ayam_kampung.length).toFixed(1);
    const avgTua = (data.ayam_tua.reduce((a, b) => a + b, 0) / data.ayam_tua.length).toFixed(1);
    
    console.log('  Avg Potong:', avgPotong);
    console.log('  Avg Kampung:', avgKampung);
    console.log('  Avg Tua:', avgTua);
    
    // Try multiple times to find elements
    let attempts = 0;
    const maxAttempts = 5;
    
    const tryUpdate = () => {
        attempts++;
        console.log(`  Attempt ${attempts} to find elements...`);
        
        const elPotong = document.getElementById('statPotong');
        const elKampung = document.getElementById('statKampung');
        const elTua = document.getElementById('statTua');
        
        console.log('  Elements found:', {
            potong: !!elPotong,
            kampung: !!elKampung,
            tua: !!elTua
        });
        
        if (elPotong && elKampung && elTua) {
            console.log('  Setting values...');
            elPotong.textContent = avgPotong;
            elKampung.textContent = avgKampung;
            elTua.textContent = avgTua;
            
            console.log('  Values set:', {
                potong: elPotong.textContent,
                kampung: elKampung.textContent,
                tua: elTua.textContent
            });
            
            console.log('✅ Stats updated successfully!');
            return true;
        } else {
            console.warn('  Elements not found yet...');
            if (attempts < maxAttempts) {
                setTimeout(tryUpdate, 50);
            } else {
                console.error('❌ Failed to find elements after', maxAttempts, 'attempts');
            }
            return false;
        }
    };
    
    tryUpdate();
}

// Update chart
function updateChart(data) {
    console.log('📈 Starting chart update...');
    
    const canvas = document.getElementById('predictionChart');
    if (!canvas) {
        console.error('❌ Canvas element not found!');
        return;
    }
    
    if (typeof Chart === 'undefined') {
        console.error('❌ Chart.js not loaded!');
        alert('Chart.js library tidak ter-load. Refresh halaman.');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    console.log('  Canvas context:', ctx);
    
    if (predictionChart) {
        console.log('  Destroying old chart...');
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
    
    console.log('✅ Chart created successfully!');
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
let dataLoaded = false;

function initDashboard() {
    if (dataLoaded) {
        console.log('⏭️ Data already loaded, skipping...');
        return;
    }
    
    console.log('🚀 Initializing dashboard...');
    
    // Pastikan semua element ada
    const statPotong = document.getElementById('statPotong');
    const statKampung = document.getElementById('statKampung');
    const statTua = document.getElementById('statTua');
    const chart = document.getElementById('predictionChart');
    const table = document.getElementById('tableBody');
    
    console.log('🔍 Checking elements:', {
        statPotong: !!statPotong,
        statKampung: !!statKampung,
        statTua: !!statTua,
        chart: !!chart,
        table: !!table
    });
    
    if (statPotong && statKampung && statTua && chart && table) {
        console.log('✅ All elements found, loading predictions...');
        dataLoaded = true;
        loadPredictions();
    } else {
        console.warn('⚠️ Some elements not found, will retry...');
    }
}

// Test function untuk debugging
function testUpdate() {
    console.log('🧪 Testing manual update...');
    
    const elPotong = document.getElementById('statPotong');
    const elKampung = document.getElementById('statKampung');
    const elTua = document.getElementById('statTua');
    
    console.log('Elements:', { elPotong, elKampung, elTua });
    
    if (elPotong) {
        elPotong.textContent = '22.7';
        console.log('✅ Updated Potong to:', elPotong.textContent);
    }
    if (elKampung) {
        elKampung.textContent = '9.8';
        console.log('✅ Updated Kampung to:', elKampung.textContent);
    }
    if (elTua) {
        elTua.textContent = '5.5';
        console.log('✅ Updated Tua to:', elTua.textContent);
    }
    
    // Also try to reload data
    loadPredictions();
}

// Try both DOMContentLoaded and window.onload
document.addEventListener('DOMContentLoaded', initDashboard);
window.addEventListener('load', initDashboard);
