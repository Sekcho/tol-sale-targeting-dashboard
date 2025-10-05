# 🚀 Deployment Guide - Render Free Tier

คู่มือการ Deploy TOL Sales Dashboard บน Render (Free tier)

## 📋 สิ่งที่เตรียมไว้แล้ว

✅ **ไฟล์ที่สร้างให้:**
- `config.py` - Environment variables management
- `db.py` - PostgreSQL database models (User, UserLog, ActiveSession)
- `logger.py` - Logging functions
- `requirements.txt` - Updated with production dependencies
- `Procfile` - Gunicorn configuration
- `render.yaml` - Render deployment config
- `.env.example` - Template for environment variables
- `.gitignore` - Git ignore rules

## ⚠️ สิ่งสำคัญ - Code Safety

**app_sales_v2.py ยังใช้งานได้ปกติ 100%!**
- ไม่ได้แก้ไข app_sales_v2.py
- ไฟล์ใหม่ทั้งหมดเป็น "optional"
- ถ้าไม่ deploy ก็ยังใช้งานแบบเดิมได้

---

## 🎯 Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
# Initialize git (if not done)
cd D:\2025\Dash\TOL_Login_Dash
git init

# Add all files
git add .

# Commit
git commit -m "feat: add production deployment support with PostgreSQL logging"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/tol-sales-dashboard.git
git branch -M main
git push -u origin main
```

### 2. Create Render Account

1. ไปที่ https://render.com
2. Sign up ด้วย GitHub account
3. Authorize Render ให้เข้าถึง repositories

### 3. Create PostgreSQL Database (Free)

1. ใน Render Dashboard → คลิก **"New +"** → **"PostgreSQL"**
2. ตั้งค่า:
   - **Name:** `tol-sales-db`
   - **Database:** `tol_sales`
   - **User:** `tol_admin` (auto-generated)
   - **Region:** Singapore (ใกล้ที่สุด)
   - **Plan:** **Free**
3. คลิก **"Create Database"**
4. รอ 2-3 นาที จนสถานะเป็น **"Available"**
5. **เก็บ Internal Database URL** (จะใช้ในขั้นต่อไป)

### 4. Create Web Service

1. ใน Render Dashboard → คลิก **"New +"** → **"Web Service"**
2. เลือก GitHub repository: `tol-sales-dashboard`
3. ตั้งค่า:

**Basic:**
- **Name:** `tol-sales-dashboard`
- **Region:** Singapore
- **Branch:** main
- **Root Directory:** (ว่างไว้)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app_sales_v2:server --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

**Plan:**
- เลือก **Free**

4. คลิก **"Advanced"** → **"Add Environment Variable"**

เพิ่ม Environment Variables ต่อไปนี้:

```
FLASK_ENV=production
DEBUG=False
SESSION_COOKIE_SECURE=True
```

**สำคัญ! เพิ่ม DATABASE_URL:**
```
DATABASE_URL=<paste Internal Database URL from Step 3>
```

**Generate SECRET_KEY:**
```python
# รันคำสั่งนี้ใน local terminal
python -c "import secrets; print(secrets.token_hex(32))"

# เอา output ไปใส่เป็น
SECRET_KEY=<output ที่ได้>
```

5. คลิก **"Create Web Service"**

### 5. รอ Deployment

1. Render จะ build และ deploy อัตโนมัติ
2. ดู logs ใน **"Logs"** tab
3. รอจน status เป็น **"Live"** (ประมาณ 5-10 นาที)

### 6. ทดสอบ

1. คลิก URL ที่ Render ให้มา (จะเป็น `https://tol-sales-dashboard.onrender.com`)
2. ควรเห็นหน้า Login
3. Login ด้วย:
   - Username: `admin`
   - Password: `admin123`

---

## 📊 ฟีเจอร์ที่พร้อมใช้งาน

### ✅ ที่ทำงานแล้ว (โดยไม่ต้องแก้ app_sales_v2.py)

1. **Production Server** - Gunicorn with 2 workers
2. **Security** - Secret key, secure cookies
3. **Database Ready** - PostgreSQL models ถูกสร้างแล้ว

### 🔄 ที่ต้องเพิ่ม (ถ้าต้องการ Logging + Analytics)

ต้องแก้ `app_sales_v2.py` เพิ่มเติม:
1. Import modules ใหม่
2. Initialize database
3. เพิ่ม logging calls
4. เพิ่ม Stats page
5. เพิ่ม User Management

**ดู PRODUCTION_INTEGRATION.md สำหรับรายละเอียด**

---

## 🎯 Render Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| **Sleep** | After 15 minutes of inactivity |
| **Wake Up** | 30-60 seconds |
| **Disk** | Temporary (reset on restart) |
| **Database** | 1GB PostgreSQL |
| **Bandwidth** | 100GB/month |
| **Build Minutes** | 400 minutes/month |

**หมายเหตุ:**
- Service จะ sleep หลัง 15 นาที ไม่มีคนใช้
- ครั้งแรกที่เข้าจะใช้เวลา 30-60 วินาที (wake up)
- เหมาะสำหรับทดสอบและใช้งานไม่หนัก (20 users)
- ถ้าต้องการ always-on → Upgrade เป็น $7/month

---

## 🔧 Troubleshooting

### ปัญหา: Build Failed

**ตรวจสอบ:**
```bash
# ใน Logs tab ของ Render
# ดูว่า error ตรงไหน
# มักจะเป็น:
# 1. requirements.txt ผิด
# 2. Python version ไม่ตรง
```

**แก้:**
```bash
# ลองรัน local
pip install -r requirements.txt
```

### ปัญหา: Application Error

**ตรวจสอบ:**
- Environment variables ครบหรือไม่
- DATABASE_URL ถูกต้องหรือไม่

**แก้:**
```python
# เช็คใน app logs
# ดูว่า error message บอกอะไร
```

### ปัญหา: Database Connection Failed

**แก้:**
```
# ตรวจสอบ DATABASE_URL
# ต้องเป็น postgresql:// (ไม่ใช่ postgres://)
# config.py จะ auto-fix ให้
```

---

## 📞 Support

**Render Documentation:**
- https://render.com/docs
- https://render.com/docs/free

**Questions?**
- Check PRODUCTION_INTEGRATION.md for advanced features
- Check logs in Render dashboard

---

**Last Updated:** 2025-10-05
**Version:** 1.0 - Basic Deployment (No app changes)
