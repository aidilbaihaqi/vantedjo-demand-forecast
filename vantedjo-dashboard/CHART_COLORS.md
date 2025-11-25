# Chart Colors - Dashboard Vantedjo

## 🎨 Warna Chart yang Digunakan

Chart menggunakan warna cerah yang kontras dengan dark background agar mudah terlihat dan dibedakan.

### **Color Palette:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CHART COLOR SCHEME                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Ayam Potong:   ━━━━━━━━  #60a5fa  (Bright Blue)          │
│                 Background: rgba(96, 165, 250, 0.1)        │
│                 Point Border: #1e40af (Dark Blue)          │
│                                                             │
│  Ayam Kampung:  ━━━━━━━━  #34d399  (Bright Green)         │
│                 Background: rgba(52, 211, 153, 0.1)        │
│                 Point Border: #047857 (Dark Green)         │
│                                                             │
│  Ayam Tua:      ━━━━━━━━  #fbbf24  (Bright Yellow)        │
│                 Background: rgba(251, 191, 36, 0.1)        │
│                 Point Border: #b45309 (Dark Orange)        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Kenapa Warna Ini?

### **1. Kontras Tinggi**
- Warna cerah terlihat jelas di dark background (#1a1a1a)
- Mudah dibedakan satu sama lain
- Tidak menyakiti mata

### **2. Color Psychology**
- **Biru (#60a5fa)**: Professional, trust, stability
  - Cocok untuk Ayam Potong (produk utama)
- **Hijau (#34d399)**: Growth, fresh, natural
  - Cocok untuk Ayam Kampung (organik)
- **Kuning (#fbbf24)**: Attention, energy, warmth
  - Cocok untuk Ayam Tua (kategori khusus)

### **3. Accessibility**
- ✅ WCAG AA compliant untuk contrast ratio
- ✅ Color-blind friendly (bisa dibedakan)
- ✅ Tidak terlalu terang (tidak menyilaukan)

## 📊 Visual Preview:

```
Chart dengan Dark Background:

30 ┤                                                         
25 ┤  ╭─╮ ╭─╮ ╭─╮  ← Ayam Potong (Biru Cerah)
20 ┤  │ ╰─╯ ╰─╯ │                                           
15 ┤  │         │  ╭─╮ ╭─╮  ← Ayam Kampung (Hijau Cerah)
10 ┤  │         ╰──╯ ╰─╯ │                                  
 5 ┤  │                 ╰─╮ ╭─╮  ← Ayam Tua (Kuning Cerah)
 0 ┴──┴─────────────────────╰─╯                            
   2  4  6  8  10  12  14                                   
```

## 🎨 Detail Styling:

### **Line Properties:**
```javascript
borderWidth: 2.5        // Garis cukup tebal untuk terlihat
tension: 0.4            // Smooth curve
fill: true              // Area di bawah garis terisi
```

### **Point Properties:**
```javascript
pointRadius: 4          // Ukuran point normal
pointHoverRadius: 6     // Ukuran point saat hover
pointBorderWidth: 2     // Border point untuk depth
```

### **Background Fill:**
```javascript
// Transparansi 0.1 agar tidak terlalu solid
backgroundColor: 'rgba(96, 165, 250, 0.1)'
```

## 🔄 Alternatif Warna (Jika Ingin Ganti):

### **Opsi 1: Pastel Bright**
```javascript
Ayam Potong:   '#818cf8'  // Indigo
Ayam Kampung:  '#a78bfa'  // Purple
Ayam Tua:      '#fb7185'  // Pink
```

### **Opsi 2: Neon**
```javascript
Ayam Potong:   '#22d3ee'  // Cyan
Ayam Kampung:  '#a3e635'  // Lime
Ayam Tua:      '#fb923c'  // Orange
```

### **Opsi 3: Warm Tones**
```javascript
Ayam Potong:   '#f87171'  // Red
Ayam Kampung:  '#fbbf24'  // Amber
Ayam Tua:      '#fb923c'  // Orange
```

## 💡 Cara Mengubah Warna:

Edit file `static/script.js`, cari bagian `datasets`:

```javascript
{
    label: 'Ayam Potong',
    borderColor: '#your-color',  // ← Ganti warna di sini
    backgroundColor: 'rgba(R, G, B, 0.1)',  // ← Sesuaikan RGB
    pointBackgroundColor: '#your-color',
    pointBorderColor: '#darker-shade',
}
```

## 🎯 Best Practices:

1. **Gunakan warna yang kontras** dengan background
2. **Jangan terlalu banyak warna** (max 3-4)
3. **Konsisten dengan brand** (jika ada)
4. **Test di berbagai device** (mobile, desktop)
5. **Pertimbangkan color-blind users**

## 📱 Responsive:

Warna chart tetap terlihat jelas di:
- ✅ Desktop (layar besar)
- ✅ Tablet (layar medium)
- ✅ Mobile (layar kecil)
- ✅ Dark mode
- ✅ Light mode (jika diubah)

## 🔍 Testing:

Untuk melihat perubahan:

```bash
# 1. Refresh browser
Ctrl + Shift + R  (hard refresh)

# 2. Atau restart server
python vantedjo-dashboard/app.py
```

## ✅ Current Status:

- [x] Warna cerah dan kontras
- [x] Mudah dibedakan
- [x] Tidak menyakiti mata
- [x] Professional look
- [x] Accessible
- [x] Responsive

---

**Result**: Chart sekarang menggunakan warna **cerah dan vibrant** yang mudah terlihat di dark background! 🎨

**Colors Used**:
- 🔵 Biru (#60a5fa) - Ayam Potong
- 🟢 Hijau (#34d399) - Ayam Kampung  
- 🟡 Kuning (#fbbf24) - Ayam Tua
