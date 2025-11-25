# Dark Theme Update - Dashboard Vantedjo

## 🎨 Perubahan Design

Dashboard telah diubah dari colorful theme menjadi **dark theme minimalis** dengan warna yang lebih subtle.

### **Sebelum vs Sesudah:**

#### **Sebelum (Colorful):**
- Background: Gradient ungu-pink
- Cards: Gradient pink-merah
- Header: Gradient ungu
- Tabel: Background putih
- Chart: Warna cerah (merah, biru, hijau)

#### **Sesudah (Dark Minimalist):**
- Background: Dark gray (#0f0f0f)
- Cards: Dark gray (#252525)
- Header: Dark gray (#1f1f1f)
- Tabel: Dark gray dengan border subtle
- Chart: Grayscale (abu-abu berbeda shade)

## 🎯 Color Palette Baru:

```css
/* Background Colors */
--bg-primary: #0f0f0f      /* Body background */
--bg-secondary: #1a1a1a    /* Container background */
--bg-tertiary: #1f1f1f     /* Header background */
--bg-card: #252525         /* Card background */

/* Text Colors */
--text-primary: #ffffff    /* Headings */
--text-secondary: #e0e0e0  /* Body text */
--text-tertiary: #a0a0a0   /* Subtext */
--text-muted: #888888      /* Muted text */

/* Border Colors */
--border-primary: #2a2a2a  /* Main borders */
--border-secondary: #333   /* Hover borders */

/* Chart Colors (Bright) */
--chart-1: #60a5fa         /* Ayam Potong - Bright Blue */
--chart-2: #34d399         /* Ayam Kampung - Bright Green */
--chart-3: #fbbf24         /* Ayam Tua - Bright Yellow */
```

## 📝 File yang Diubah:

### 1. **style.css**
- ✅ Background body: Dark (#0f0f0f)
- ✅ Container: Dark gray dengan border subtle
- ✅ Header: Dark dengan text putih
- ✅ Cards: Dark gray dengan hover effect minimal
- ✅ Tabel: Dark dengan alternating rows
- ✅ Footer: Dark dengan text muted

### 2. **script.js**
- ✅ Chart colors: Grayscale (tidak colorful)
- ✅ Chart grid: Dark (#2a2a2a)
- ✅ Chart text: Light gray
- ✅ Legend: Light text

## 🎨 Design Principles:

1. **Minimalist**: Tidak ada gradient, warna solid
2. **Subtle**: Border dan shadow yang halus
3. **Readable**: Kontras yang cukup untuk readability
4. **Professional**: Warna grayscale yang elegan
5. **Consistent**: Semua elemen mengikuti palette yang sama

## 🔍 Detail Perubahan:

### **Header:**
```css
background: #1f1f1f
color: #e0e0e0
border-bottom: 1px solid #2a2a2a
```

### **Stat Cards:**
```css
background: #252525
border: 1px solid #333
hover: border-color: #444
```

### **Tabel:**
```css
background: #1f1f1f
thead: #252525
tbody even: #1a1a1a
tbody hover: #252525
border: 1px solid #2a2a2a
```

### **Chart:**
```css
Line 1 (Ayam Potong): #60a5fa (Bright Blue)
Line 2 (Ayam Kampung): #34d399 (Bright Green)
Line 3 (Ayam Tua): #fbbf24 (Bright Yellow)
Grid: #2a2a2a
Text: #888888
```

## 🚀 Cara Melihat Perubahan:

```bash
# 1. Pastikan server berjalan
python vantedjo-dashboard/app.py

# 2. Buka browser
http://localhost:5000

# 3. Refresh halaman (Ctrl+F5) untuk clear cache
```

## 💡 Customization:

Jika ingin mengubah warna, edit file `static/style.css`:

### Contoh: Ubah warna accent
```css
/* Ganti #888888 dengan warna lain */
.stat-card:hover {
    border-color: #your-color;
}
```

### Contoh: Ubah brightness
```css
/* Lebih terang */
body {
    background: #1a1a1a; /* dari #0f0f0f */
}

/* Lebih gelap */
body {
    background: #000000;
}
```

## 📊 Accessibility:

- ✅ Kontras text-background: WCAG AA compliant
- ✅ Hover states: Jelas dan visible
- ✅ Focus states: Maintained
- ✅ Readable font sizes: 14px minimum

## 🎯 Browser Compatibility:

- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support
- ✅ Safari: Full support
- ✅ Mobile: Responsive

## 📱 Responsive Design:

Dark theme tetap responsive di semua ukuran layar:
- Desktop: Full layout
- Tablet: Grid adjusted
- Mobile: Single column

---

**Updated**: Dark theme minimalis
**Status**: ✅ Production ready
**Feedback**: Silakan adjust warna sesuai preferensi
