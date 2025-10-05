# TOL Sales Dashboard Project

## ภาพรวม Project
Dashboard สำหรับทีมขายในการวิเคราะห์และวางแผนการขายตามพื้นที่ โดยใช้ข้อมูล Potential Score, Port Utilization และข้อมูลอื่นๆ

**Production URL:** https://tol-sales-dashboard.onrender.com

## โครงสร้างไฟล์

```
TOL_Login_Dash/
├── app.py                          # Dashboard หลัก (ใช้ OpenStreetMap)
├── app_sales.py                    # Sales Journey version (มีตารางและ Navigate)
├── app_sales_v2.py                 # Sales Journey v2 - Production (Responsive + DB + Analytics) ⭐
├── models.py                       # Database models (User, PageView, ActivityLog)
├── init_db.py                      # Database initialization script
├── build.sh                        # Render build script
├── runtime.txt                     # Python version specification
├── .python-version                 # Python version for Render
├── render.yaml                     # Render configuration
├── requirements.txt                # Python dependencies
├── templates/
│   ├── login.html                  # Login page
│   ├── register.html               # User registration (Admin only)
│   └── admin_stats.html            # Admin statistics dashboard
├── static/                         # Static files (images, etc.)
├── auth/                           # Legacy auth folder
│   └── models.py                   # Old user models
├── Prepared_True_Dataset_Updated.csv  # ข้อมูลหลัก
├── POTENTIAL_SCORE_CRITERIA.md     # สูตรและ criteria การคำนวณคะแนน
├── USER_MANUAL.md                  # คู่มือการใช้งานสำหรับ user
└── README.md                       # เอกสารนี้
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

### app_sales_v2.py (Sales Journey v2 - Production) ⭐ แนะนำ
**ทุกฟีเจอร์จาก app_sales.py + ฟีเจอร์ใหม่:**

#### UI/UX Features:
- ✨ **Responsive Design** - รองรับ Mobile, Tablet, iPad, Desktop
- 📱 **Mobile-First UI** - ออกแบบให้ใช้งานบนมือถือได้ลื่นไหล
- 🎨 **Bootstrap Theme** - UI สวยงาม มืออาชีพ เป็นสัดส่วน
- 📂 **Collapsible Filters** - ซ่อน/แสดง Filter บนมือถือเพื่อประหยัดพื้นที่
- 🔝 **Sticky Navbar** - เมนูบนคงที่ เข้าถึงง่าย
- 📏 **Smart Layout** - ปรับขนาดอัตโนมัติตามหน้าจอ

#### Backend Features:
- 🗄️ **Database Integration** - PostgreSQL (Production) / SQLite (Development)
- 👥 **User Management** - Role-based access control (Admin/User)
- 📊 **Analytics & Logging** - Page views, Activity logs, User statistics
- 🔐 **Secure Authentication** - Password hashing with bcrypt
- 📝 **User Registration** - Admin can create new users

#### URLs:
- Local: `http://127.0.0.1:8051/dashboard/`
- Production: `https://tol-sales-dashboard.onrender.com/dashboard/`

## URLs ทั้งหมด (app_sales_v2.py)

### Production
- **Login:** https://tol-sales-dashboard.onrender.com/login
- **Dashboard:** https://tol-sales-dashboard.onrender.com/dashboard/
- **Register User (Admin):** https://tol-sales-dashboard.onrender.com/register
- **Admin Stats (Admin):** https://tol-sales-dashboard.onrender.com/admin/stats
- **Logout:** https://tol-sales-dashboard.onrender.com/logout

### Access Control
| URL | User | Admin |
|-----|------|-------|
| `/login` | ✅ | ✅ |
| `/dashboard/` | ✅ | ✅ |
| `/register` | ❌ | ✅ |
| `/admin/stats` | ❌ | ✅ |
| `/logout` | ✅ | ✅ |

## การติดตั้ง (Local Development)

### 1. Clone Repository
```bash
git clone https://github.com/Sekcho/tol-sale-targeting-dashboard.git
cd tol-sale-targeting-dashboard
```

### 2. สร้าง Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python init_db.py
```
จะสร้างไฟล์ `app.db` (SQLite) และ default users:
- Admin: `admin` / `admin123`
- User: `user` / `password`

### 5. รันแอพ

**Sales Journey v2 (Production - แนะนำ):**
```bash
python app_sales_v2.py
```

**Dashboard อื่นๆ (Legacy):**
```bash
python app.py          # Dashboard หลัก
python app_sales.py    # Sales Journey v1
```

เปิดเบราว์เซอร์:
- app_sales_v2.py: `http://127.0.0.1:8051/login`
- app.py และ app_sales.py: `http://127.0.0.1:8050/login`

**Default Login:**
- Username: `admin` | Password: `admin123`
- Username: `user` | Password: `password`

## Production Deployment (Render)

### Database Setup
1. สร้าง PostgreSQL database บน Render
2. Copy Internal Database URL
3. เพิ่ม Environment Variable: `DATABASE_URL`

### Environment Variables
```bash
DATABASE_URL=postgresql://...  # จาก Render PostgreSQL
SECRET_KEY=your-secret-key     # Random string
FLASK_ENV=production
```

### Build & Deploy
Render จะใช้ `build.sh` อัตโนมัติ:
1. Install dependencies
2. Initialize database
3. Start gunicorn server

## ฟีเจอร์หลัก

### 1. Authentication & User Management
- 🔐 Login/Logout system with Flask-Login
- 👤 Role-based access control (Admin/User)
- 🔑 Password hashing with bcrypt
- 📝 User registration (Admin only)
- 🚪 Protected routes with decorators

### 2. Data Visualization
- 🗺️ Interactive map with bubble markers
- 🎨 Color by Potential Score (Green = High, Yellow = Medium, Red = Low)
- 📏 Size by Port Use
- 💬 Hover info แสดงข้อมูลละเอียด (Household, Port, Market Share, etc.)
- 📊 Dynamic updates based on filters

### 3. Filters
- **Quick Filters:**
  - 🔥 High Potential (>70)
  - 📍 Show All
- **Location Filters (Cascading):**
  - Province → District → Sub-district → Happy Block
- **Range Sliders:**
  - Net Add (ลูกค้าเพิ่มใหม่)
  - Potential Score (0-100)
  - Port Utilization (%)
  - Market Share True (%)
  - L2 Aging (เดือน)

### 4. Sales Journey Features
- 🎯 Quick Filter: High Potential (>70)
- 📋 Location Table (sortable, paginated, 10 items/page)
- 🗺️ Navigate buttons → Google Maps with directions
- 🎨 Color-coded rows by Potential Score:
  - 🟢 Green: ≥70 (High priority)
  - 🟡 Yellow: 50-69 (Medium)
  - 🔴 Red: <50 (Low)
- 📱 Mobile-optimized navigation

### 5. Analytics & Monitoring (Admin Only)
- 📊 **Page View Counter**
  - Track visits to each page
  - Last viewed timestamp
- 📝 **Activity Logs**
  - Login/logout tracking
  - Dashboard views
  - Failed login attempts
  - IP address and User-Agent logging
- 👥 **User Statistics**
  - Total users
  - Login count per user
  - Last login timestamp
  - Role distribution

### 6. Database Features
- 🗄️ PostgreSQL (Production) / SQLite (Development)
- 💾 Persistent user accounts
- 📊 Historical analytics data
- 🔄 Auto-migration on deployment

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

### Backend
- **Framework:** Flask 3.0.3
- **Authentication:** Flask-Login 0.6.3, Flask-Bcrypt 1.0.1
- **Database:**
  - PostgreSQL (Production) via psycopg2-binary 2.9.10
  - SQLite (Development)
- **ORM:** Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.43
- **Server:** Gunicorn 21.2.0 (Production)

### Frontend
- **Framework:** Dash 2.18.2, Plotly 5.24.1
- **Components:** Dash Bootstrap Components 1.6.0
- **UI:** Bootstrap 5, Responsive Design

### Data Processing
- **Libraries:** Pandas 2.2.3, NumPy 2.2.2
- **Visualization:** Plotly Mapbox (OpenStreetMap)

### Deployment
- **Platform:** Render.com
- **Python:** 3.11.11
- **Database:** PostgreSQL 14+

## เอกสารประกอบ

- 📖 [USER_MANUAL.md](./USER_MANUAL.md) - คู่มือการใช้งานสำหรับ user
- 📊 [POTENTIAL_SCORE_CRITERIA.md](./POTENTIAL_SCORE_CRITERIA.md) - สูตรและ criteria การคำนวณคะแนน
- 🗂️ [README.md](./README.md) - เอกสารนี้ (Technical documentation)

## License

Internal use only - True Corporation

## Contact

สำหรับคำถามหรือข้อเสนอแนะ:
- GitHub Repository: https://github.com/Sekcho/tol-sale-targeting-dashboard
- Production URL: https://tol-sales-dashboard.onrender.com

---

**Last Updated:** 2025-10-05
**Version:** 3.0 (Production Deployment with Full User Management & Analytics)
**Python Version:** 3.11.11
**Main App:** `app_sales_v2.py`
