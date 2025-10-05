# Quick Start Guide

คู่มือเริ่มต้นใช้งานอย่างรวดเร็ว

## 🚀 เริ่มต้นใน 5 นาที

### 1. ติดตั้ง Dependencies (1 นาที)
```bash
cd D:\2025\Dash\TOL_Login_Dash
pip install -r requirements.txt
```

### 2. รันแอพ (30 วินาที)

**Dashboard หลัก:**
```bash
python app.py
```

**Sales Journey:**
```bash
python app_sales.py
```

**Sales Journey v2 - Responsive (แนะนำสำหรับ Sales บนมือถือ/iPad):**
```bash
python app_sales_v2.py
```

### 3. เปิดเบราว์เซอร์ (30 วินาที)

**app.py และ app_sales.py:**
```
http://127.0.0.1:8050/login
```

**app_sales_v2.py:**
```
http://127.0.0.1:8051/login
```

### 4. Login (30 วินาที)
- **Username:** `admin`
- **Password:** `admin123`

### 5. เริ่มใช้งาน! 🎉

---

## 📱 สำหรับ Sales (ใช้ app_sales.py)

### วิธีหาจุดขาย High Potential

1. **คลิกปุ่ม "🔥 High Potential Only"**
   - จะแสดงเฉพาะจุดที่มี Potential Score > 70

2. **ดูตารางด้านล่างแผนที่**
   - เรียงลำดับจากคะแนนสูงสุด → ต่ำสุด
   - แถวสีเขียว = คะแนนสูง

3. **คลิก "🗺️ Open Maps" ในตาราง**
   - จะเปิดแอพ Google Maps
   - เส้นทางไปยังจุดนั้นๆ

4. **เดินทางไป!**

---

## 🗺️ การใช้งานแผนที่

### Zoom
- **Scroll mouse wheel** = ซูมเข้า/ออก
- **Double click** = รีเซ็ต zoom

### Pan (เลื่อนแผนที่)
- **ลากเมาส์** = เลื่อนแผนที่

### ดูข้อมูล
- **Hover บน bubble** = แสดงข้อมูลละเอียด

---

## 🎯 Filter คู่มือฉบับย่อ

### Location Filters (เลือกตามลำดับ)
1. **Province** → เลือกจังหวัด
2. **District** → เลือกอำเภอ (จะแสดงเฉพาะอำเภอในจังหวัดที่เลือก)
3. **Sub-district** → เลือกตำบล
4. **Happy Block** → เลือก block

### Quick Filters (app_sales.py only)
- **🔥 High Potential Only** = แสดงเฉพาะ Potential Score > 70
- **📍 Show All** = แสดงทั้งหมด

### Advanced Filters
- **Net Add** = จำนวนผู้ใช้เพิ่มขึ้น
- **Potential Score** = คะแนนความน่าสนใจ (0-100)
- **% Port Utilize** = เปอร์เซ็นต์การใช้งาน Port
- **Market Share True** = ส่วนแบ่งการตลาดของ True
- **L2 Aging** = อายุของ L2 (เดือน)

---

## 🎨 สีบนแผนที่

### Bubble Color (สีของวงกลม)
- 🔵 **น้ำเงินเข้ม** = Potential Score สูง
- 🔷 **น้ำเงินกลาง** = Potential Score ปานกลาง
- ⚪ **น้ำเงินอ่อน** = Potential Score ต่ำ

### Bubble Size (ขนาดของวงกลม)
- **ใหญ่** = Port Use มาก
- **เล็ก** = Port Use น้อย

### Table Row Color (app_sales.py)
- 🟢 **เขียว** = Potential Score ≥ 70 (ดีมาก)
- 🟡 **เหลือง** = Potential Score 50-69 (ปานกลาง)
- 🔴 **แดง** = Potential Score < 50 (ต่ำ)

---

## 💡 Tips & Tricks

### 1. หาจุดที่มี Port Available เยอะ
```
1. ปรับ "% Port Utilize" ให้ต่ำ (0-50%)
2. ดูที่ตาราง column "✅ Available"
3. เลือกจุดที่มี Available มาก
```

### 2. หาพื้นที่ที่ Net Add เติบโต
```
1. ปรับ "Net Add Filter" ให้สูง (>5)
2. ดูแผนที่ว่าจุดไหนมีลูกค้าเพิ่มขึ้นเยอะ
```

### 3. หาพื้นที่ที่ L2 ใหม่
```
1. ปรับ "L2 Aging" ให้ต่ำ (0-12 เดือน)
2. พื้นที่เหล่านี้น่าจะมีโอกาสขายดี
```

### 4. วางแผนเส้นทาง (Manual)
```
1. กด "🔥 High Potential Only"
2. ดูตารางด้านล่าง (เรียงตามคะแนนแล้ว)
3. เลือก 3-5 จุดที่อยู่ใกล้กัน
4. คลิก "🗺️ Open Maps" ทีละจุด
5. บันทึก waypoints ใน Google Maps
```

---

## ⚠️ Troubleshooting

### แผนที่ไม่แสดงข้อมูล
**สาเหตุ:** Filter กรองข้อมูลหมดทั้งหมด
**วิธีแก้:** กด "📍 Show All" หรือ ปรับ filter ให้กว้างขึ้น

### Navigate button ไม่ทำงาน
**สาเหตุ:** Browser block pop-up
**วิธีแก้:** อนุญาต pop-up สำหรับเว็บไซต์นี้

### Zoom/Pan ไม่ได้
**สาเหตุ:** Browser compatibility
**วิธีแก้:** ใช้ Chrome, Firefox หรือ Edge เวอร์ชันล่าสุด

### Login ไม่ได้
**สาเหตุ:** Username/Password ผิด
**วิธีแก้:** ใช้ `admin` / `admin123` หรือ `user` / `password`

---

## 📞 ติดต่อ

**ปัญหาเร่งด่วน:** [Emergency Contact]
**คำถามทั่วไป:** [General Contact]
**Bug Report:** [GitHub Issues / Email]

---

## 🔗 ลิงก์เพิ่มเติม

- [README.md](README.md) - รายละเอียดทั้งหมด
- [CHANGELOG.md](CHANGELOG.md) - ประวัติการพัฒนา
- [DEVELOPMENT.md](DEVELOPMENT.md) - คู่มือสำหรับนักพัฒนา

---

## 📱 สำหรับ app_sales_v2.py (Responsive Version)

### ความแตกต่างจาก app_sales.py

**ฟีเจอร์เพิ่มเติม:**
- ✨ **Responsive Layout** - รองรับ Mobile, Tablet, iPad, Desktop
- 🔝 **Sticky Navbar** - เมนูบนคงที่ เข้าถึงง่าย
- 📂 **Collapsible Filters** - กดปุ่มเพื่อซ่อน/แสดง Filters
- 🎨 **Professional UI** - ใช้ Bootstrap Theme สวยงาม เป็นสัดส่วน

### วิธีใช้บนมือถือ

1. **เปิดเบราว์เซอร์บนมือถือ**
   ```
   http://192.168.x.x:8051/login
   ```
   (แทน 192.168.x.x ด้วย IP ของคอมพิวเตอร์ที่รันแอพ)

2. **Filter จะ Stack ด้านบน**
   - คลิกปุ่ม "📍 Location" เพื่อแสดง/ซ่อน Location Filters
   - คลิกปุ่ม "🎯 Quick" เพื่อแสดง/ซ่อน Quick Filters
   - คลิกปุ่ม "⚙️ Advanced" เพื่อแสดง/ซ่อน Advanced Filters

3. **แผนที่และตารางจะแสดงเต็มหน้าจอ**
   - Scroll ลงเพื่อดูตาราง
   - Pinch to zoom บนแผนที่
   - คลิก "🗺️ Open Maps" เพื่อ Navigate

### Layout แต่ละอุปกรณ์

**Mobile (<768px):**
```
┌────────────────┐
│   Navbar       │ ← Sticky
├────────────────┤
│   Filters      │ ← 100% width, Collapsible
├────────────────┤
│   Map          │ ← 100% width
├────────────────┤
│   Table        │ ← 100% width
└────────────────┘
```

**Tablet (768px-991px):**
```
┌──────────────────────────┐
│   Navbar                 │ ← Sticky
├────────┬─────────────────┤
│ Filter │  Map            │ ← 33% / 67%
│ (33%)  │  (67%)          │
│        ├─────────────────┤
│        │  Table          │
└────────┴─────────────────┘
```

**Desktop (≥992px):**
```
┌──────────────────────────┐
│   Navbar                 │ ← Sticky
├──────┬───────────────────┤
│Filter│  Map              │ ← 25% / 75%
│(25%) │  (75%)            │
│      ├───────────────────┤
│      │  Table            │
└──────┴───────────────────┘
```

---

**Last Updated:** 2025-10-05
**Version:** 2.1 (Responsive Update)
