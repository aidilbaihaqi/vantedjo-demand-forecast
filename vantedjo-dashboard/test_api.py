"""
Script untuk testing API dashboard
Jalankan: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_predictions():
    """Test endpoint prediksi"""
    print("Testing /api/predictions...")
    response = requests.get(f"{BASE_URL}/api/predictions")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Success!")
        print(f"  Period: {data['period']}")
        print(f"  Dates: {len(data['data']['dates'])} hari")
        print(f"  Ayam Potong avg: {sum(data['data']['ayam_potong'])/len(data['data']['ayam_potong']):.2f}")
        print(f"  Ayam Kampung avg: {sum(data['data']['ayam_kampung'])/len(data['data']['ayam_kampung']):.2f}")
        print(f"  Ayam Tua avg: {sum(data['data']['ayam_tua'])/len(data['data']['ayam_tua']):.2f}")
    else:
        print(f"✗ Failed: {response.status_code}")
    print()

def test_historical():
    """Test endpoint data historis"""
    print("Testing /api/historical...")
    response = requests.get(f"{BASE_URL}/api/historical")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Success!")
        print(f"  Historical data: {len(data['data']['dates'])} hari")
    else:
        print(f"✗ Failed: {response.status_code}")
    print()

def test_stats():
    """Test endpoint statistik"""
    print("Testing /api/stats...")
    response = requests.get(f"{BASE_URL}/api/stats")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Success!")
        for category, stats in data['data'].items():
            print(f"  {category}:")
            print(f"    - Average: {stats['average']}")
            print(f"    - Max: {stats['max']}")
            print(f"    - Min: {stats['min']}")
    else:
        print(f"✗ Failed: {response.status_code}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Dashboard API Testing")
    print("=" * 50)
    print()
    
    try:
        test_predictions()
        test_historical()
        test_stats()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("✗ Error: Tidak dapat terhubung ke server")
        print("  Pastikan server sudah berjalan dengan: python app.py")
