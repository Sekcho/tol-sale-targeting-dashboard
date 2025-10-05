# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-10-05

### Added - Responsive Design (app_sales_v2.py)
- ✨ **app_sales_v2.py** - เวอร์ชัน Responsive สำหรับ Mobile, Tablet, Desktop
- 📱 **Mobile-First Design** - รองรับการใช้งานบนมือถือ, iPad, Tablet
- 🎨 **Bootstrap Integration** - ใช้ Dash Bootstrap Components
  - Bootstrap Theme (BOOTSTRAP)
  - Responsive grid system (xs, sm, md, lg)
  - Meta viewport tag สำหรับ mobile
- 🔝 **Sticky Navbar** - เมนูบนคงที่ พร้อมปุ่ม Logout
- 📂 **Collapsible Filters** - ซ่อน/แสดง Filter sections
  - Location Filters (Province, District, Sub-district, Happy Block)
  - Quick Filters (High Potential, Show All)
  - Advanced Filters (Net Add, Potential Score, Port Utilize, Market Share, L2 Aging)
- 📏 **Smart Responsive Layout**
  - Mobile (xs): Stack ทั้งหมด 100% width
  - Tablet (md): Filters 33% / Map+Table 67%
  - Desktop (lg): Filters 25% / Map+Table 75%
- 🎯 **Professional UI**
  - Card-based design
  - Proper spacing และ margins
  - Smaller font sizes สำหรับ mobile
  - Map height ปรับเป็น 500px เหมาะกับหน้าจอเล็ก

### Changed
- 🔢 **Port Number** - app_sales_v2.py ใช้ port 8051 (ไม่ชนกับ 8050)
- 📦 **Dependencies** - เพิ่ม dash-bootstrap-components==2.0.4

### Technical Details
- ใช้ `dbc.Container(fluid=True)` สำหรับ full-width
- ใช้ `dbc.Row` และ `dbc.Col` สำหรับ responsive grid
- Callbacks สำหรับ toggle collapsible sections
- ทุกฟีเจอร์จาก app_sales.py ยังคงใช้งานได้ปกติ

## [2.0.0] - 2025-10-05

### Added - Sales Journey Features (app_sales.py)
- ✨ สร้าง `app_sales.py` แยกออกจาก `app.py` เพื่อป้องกัน code เดิมพัง
- 📋 **Location Table** - ตารางรายการจุดขายด้านล่างแผนที่
  - เรียงลำดับตาม Potential Score (สูง → ต่ำ)
  - Sortable columns
  - Pagination (10 items/page)
- 🗺️ **Navigate Button** - คลิกเพื่อเปิด Google Maps แอพ
  - ใช้งานได้ทั้งบนมือถือและคอมพิวเตอร์
  - URL: `https://www.google.com/maps/dir/?api=1&destination=lat,lng`
- 🎨 **Color-Coded Table**
  - 🟢 เขียว = Potential Score ≥ 70 (High)
  - 🟡 เหลือง = Potential Score 50-69 (Medium)
  - 🔴 แดง = Potential Score < 50 (Low)
- 🎯 **Quick Filters**
  - "High Potential Only (>70)" button
  - "Show All" button
- 📊 **Smart Display** - แสดงจำนวนจุดและค่าเฉลี่ย Potential Score
- 🎨 **Improved UI** - Sales-friendly design with emojis and colors

### Changed
- 🗺️ แปลง color scale เป็น "Blues" (น้ำเงินเข้ม = High, อ่อน = Low)
- 🖱️ เพิ่ม `scrollZoom: true` สำหรับ mouse wheel zoom
- 📐 ปรับ layout ให้แผนที่กว้างขึ้น (68% instead of 65%)

### Fixed
- ❌ แก้ ImportError: GoogleMaps ไม่มีใน dash_extensions
  - Solution: ใช้ `px.scatter_mapbox` แทน
- 🗺️ แก้แผนที่แสดงผิดตำแหน่ง (กรุงเทพ)
  - Solution: คำนวณ center จากค่าเฉลี่ย Lat/Lon ของข้อมูลที่ filter
- 🖱️ แก้ zoom in/out ด้วย mouse ไม่ได้
  - Solution: เพิ่ม `config={'scrollZoom': True}`
- 🎨 แก้สีแผนที่ไม่ชัดเจน
  - Solution: เปลี่ยนจาก Viridis → RdYlGn → Blues

## [1.0.0] - 2025-01-25 (Initial Version)

### Added
- 🔐 Login/Logout system (Flask-Login)
- 🗺️ Interactive map with Plotly Mapbox
- 📊 Filters:
  - Province → District → Sub-district → Happy Block (cascading)
  - Net Add slider
  - Potential Score slider
  - Port Utilization slider
  - Market Share True slider
  - L2 Aging slider
- 📈 Data preprocessing and Potential Score calculation
- 🎨 Bubble visualization (size by Port Use, color by Potential Score)

### Tech Stack
- Flask 3.0.3
- Dash 2.18.2
- Plotly 5.24.1
- Pandas 2.2.3
- Flask-Login 0.6.3

## [Unreleased] - Future Features

### Planned
- 🛣️ Route Planning - เลือกหลายจุด → สร้างเส้นทางที่เหมาะสม
- ✅ Check-in System - Sales check-in เมื่อถึงจุดหมาย
- 📍 Radius Search - หาจุดภายใน 5km/10km/20km
- 📴 Offline Mode - Cache data for offline use
- 📊 Analytics Dashboard - Visit success rate, performance metrics
- 🌍 Current Location - Show user's current location on map
- 📸 Photo Upload - Upload photos at each location
- 📝 Notes - Add notes for each visit
- 🔔 Notifications - Alert when near high-potential locations

### Under Consideration
- 🗺️ Google Maps integration (requires API key & billing)
- 🎯 ML-based route optimization
- 📱 Progressive Web App (PWA)
- 🔄 Real-time collaboration
- 📊 Export to Excel/PDF

---

## Version Guide

### Version Number Format: MAJOR.MINOR.PATCH

- **MAJOR** - Breaking changes (ไม่ backward compatible)
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

### Files by Version

| Version | Main File | Sales File | Sales v2 File | Notes |
|---------|-----------|------------|---------------|-------|
| 1.0.0   | app.py    | -          | -             | Initial release |
| 2.0.0   | app.py    | app_sales.py | -           | Sales Journey features |
| 2.1.0   | app.py    | app_sales.py | app_sales_v2.py | Responsive design |

---

**Maintained by:** [Your Name]
**Last Updated:** 2025-10-05
