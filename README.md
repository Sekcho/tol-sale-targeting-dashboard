# TOL Sales Dashboard Project

## ภาพรวม Project
Dashboard สำหรับทีมขายในการวิเคราะห์และวางแผนการขายตามพื้นที่ โดยใช้ข้อมูล Potential Score, Port Utilization และข้อมูลอื่นๆ

## โครงสร้างไฟล์

```
TOL_Login_Dash/
├── app.py                          # Dashboard หลัก (ใช้ OpenStreetMap)
├── app_sales.py                    # Sales Journey version (มีตารางและ Navigate)
├── app_sales_v2.py                 # Sales Journey v2 (Responsive - Mobile/Tablet/Desktop)
├── app1.py, app2.py, applogin.py  # ไฟล์เก่า (archive)
├── database.py                     # Database configuration
├── import_users.py                 # User import script
├── requirements.txt                # Python dependencies
├── templates/
│   └── login.html                  # Login page template
├── static/                         # Static files
├── auth/
│   └── models.py                   # User models
└── Prepared_True_Dataset_Updated.csv  # ข้อมูลหลัก
```

## ความแตกต่างระหว่าง app.py, app_sales.py และ app_sales_v2.py

### app.py (Dashboard หลัก)
- แผนที่แบบ scatter_mapbox (OpenStreetMap)
- Filter แบบละเอียด
- เน้นการวิเคราะห์ข้อมูล
- URL: `http://127.0.0.1:8050/dashboard/`

### app_sales.py (Sales Journey)
- แผนที่แบบ scatter_mapbox (OpenStreetMap)
- **Quick Filters** สำหรับ High Potential
- **ตารางรายการจุดขาย** เรียงตาม Potential Score
- **ปุ่ม Navigate** เปิด Google Maps แอพ
- **Color-coded table** (เขียว/เหลือง/แดง)
- เหมาะสำหรับ Sales ในสนาม
- URL: `http://127.0.0.1:8050/dashboard/`

### app_sales_v2.py (Sales Journey v2 - Responsive) ⭐ แนะนำ
- **ทุกฟีเจอร์จาก app_sales.py**
- ✨ **Responsive Design** - รองรับ Mobile, Tablet, iPad, Desktop
- 📱 **Mobile-First UI** - ออกแบบให้ใช้งานบนมือถือได้ลื่นไหล
- 🎨 **Bootstrap Theme** - UI สวยงาม มืออาชีพ เป็นสัดส่วน
- 📂 **Collapsible Filters** - ซ่อน/แสดง Filter บนมือถือเพื่อประหยัดพื้นที่
- 🔝 **Sticky Navbar** - เมนูบนคงที่ เข้าถึงง่าย
- 📏 **Smart Layout** - ปรับขนาดอัตโนมัติตามหน้าจอ
  - Mobile: Filter + Map/Table แบบ Stack
  - Tablet: Filter 33% / Map 67%
  - Desktop: Filter 25% / Map 75%
- URL: `http://127.0.0.1:8051/dashboard/` (Port 8051)

## การติดตั้ง

### 1. สร้าง Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 3. รันแอพ

**Dashboard หลัก:**
```bash
python app.py
```

**Sales Journey:**
```bash
python app_sales.py
```

**Sales Journey v2 (Responsive - แนะนำ):**
```bash
python app_sales_v2.py
```

เปิดเบราว์เซอร์:
- app.py และ app_sales.py: `http://127.0.0.1:8050/login`
- app_sales_v2.py: `http://127.0.0.1:8051/login`

**Default Login:**
- Username: `admin` | Password: `admin123`
- Username: `user` | Password: `password`

## ฟีเจอร์หลัก

### 1. Authentication
- Login/Logout system
- Flask-Login integration
- Protected routes

### 2. Data Visualization
- Interactive map with bubble markers
- Color by Potential Score (Blues scale)
- Size by Port Use
- Hover info แสดงข้อมูลละเอียด

### 3. Filters
- **Location Filters:** Province → District → Sub-district → Happy Block
- **Range Sliders:**
  - Net Add
  - Potential Score
  - Port Utilization
  - Market Share True
  - L2 Aging

### 4. Sales Journey Features (app_sales.py only)
- 🎯 Quick Filter: High Potential (>70)
- 📋 Location Table (sortable, paginated)
- 🗺️ Navigate buttons (Google Maps integration)
- 🎨 Color-coded rows by Potential Score

## Data Preprocessing

### Potential Score Calculation
```python
Potential Score = (
    0.4 * Household Density +
    0.25 * Installation Density +
    0.2 * Net Add +
    0.05 * Market Share +
    0.1 * True Speed
) * 100
```

### Key Metrics
- **Household Density** = Household / 0.25 sq.km
- **L2 Aging** = Months since L2 Inservice date
- **Port Utilization** = (Port Use / Port Capacity) * 100

## การพัฒนาต่อ

### ฟีเจอร์ที่แนะนำ

1. **Route Planning**
   - เลือกหลายจุด → สร้างเส้นทางที่เหมาะสม
   - Multi-stop navigation

2. **Check-in System**
   - Sales check-in เมื่อถึงจุดหมาย
   - บันทึก Visit Status (visited/pending/closed)

3. **Radius Search**
   - หาจุดภายใน 5km/10km/20km จากตำแหน่งปัจจุบัน
   - Geolocation API

4. **Offline Mode**
   - Cache data สำหรับพื้นที่ที่เลือก
   - Service Worker

5. **Analytics Dashboard**
   - Visit success rate
   - Sales performance by area
   - Time spent per location

### การเพิ่ม Google Maps แท้

หากต้องการใช้ Google Maps แทน OpenStreetMap:

```python
# 1. ติดตั้ง package
pip install dash-google-maps

# 2. ได้ Google Maps API Key
# https://console.cloud.google.com/

# 3. แก้ไข app.py
fig.update_layout(
    mapbox_style="mapbox://styles/mapbox/streets-v11",
    mapbox_accesstoken="YOUR_MAPBOX_TOKEN"
)
```

**หมายเหตุ:** Google Maps มีค่าใช้จ่าย แต่มี Free tier 200 USD/เดือน

## Troubleshooting

### ปัญหาที่พบบ่อย

**1. ImportError: cannot import name 'GoogleMaps'**
- ✅ แก้แล้ว: ใช้ OpenStreetMap แทน

**2. แผนที่ไม่แสดง bubble**
- ตรวจสอบว่ามีข้อมูล Latitude/Longitude
- ตรวจสอบ filter ไม่กรองข้อมูลหมดทั้งหมด

**3. Zoom/Pan ไม่ทำงาน**
- ตรวจสอบ config={'scrollZoom': True}
- ตรวจสอบ dragmode='pan'

**4. Navigate button ไม่ทำงาน**
- ตรวจสอบว่าเบราว์เซอร์รองรับ target='_blank'
- ลองเปิดบนมือถือ (จะเปิดแอพ Google Maps โดยตรง)

## Tech Stack

- **Backend:** Flask, Flask-Login
- **Frontend:** Dash, Plotly, Dash Bootstrap Components (v2 only)
- **Data:** Pandas, NumPy
- **Map:** Plotly Mapbox (OpenStreetMap)
- **UI Framework:** Bootstrap 5 (app_sales_v2.py)

## License

Internal use only - True Corporation

## Contact

สำหรับคำถามหรือข้อเสนอแนะ:
- Project Owner: [ชื่อผู้รับผิดชอบ]
- Email: [อีเมล]

---

**Last Updated:** 2025-10-05
**Version:** 2.0 (Sales Journey Update)
