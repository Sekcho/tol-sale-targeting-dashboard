# 🔧 Production Features Integration Guide

คู่มือการเพิ่ม Logging, Analytics, และ User Management เข้ากับ app_sales_v2.py

## ⚠️ สำคัญ!

**app_sales_v2.py ยังไม่ได้ integrate features เหล่านี้**
- ต้อง deploy ก่อน (ตาม DEPLOYMENT.md)
- ทดสอบว่าใช้งานได้ปกติ
- แล้วค่อยเพิ่ม features ทีละอัน

---

## 🎯 Features ที่พร้อมใช้งาน

### ✅ ไฟล์ที่สร้างแล้ว:

1. **config.py** - Environment variables
2. **db.py** - Database models (PostgreSQL)
   - User model (username, password, role)
   - UserLog model (activity tracking)
   - ActiveSession model (online counter)
3. **logger.py** - Logging functions
   - log_login(), log_logout()
   - log_navigate(), log_filter_change()
   - log_quick_filter(), log_page_view()
   - get_user_stats(), get_recent_activity()

---

## 📝 Integration Steps

### Phase 1: Basic Integration (30 minutes)

เพิ่ม imports และ database initialization

**1. เปิด app_sales_v2.py**

**2. เพิ่ม imports ด้านบน (หลังบรรทัด 10):**

```python
# Production features (optional - will fallback if not available)
try:
    from config import get_config
    from db import db, init_db, User, get_active_users_count
    from logger import (
        log_login, log_logout, log_navigate,
        log_filter_change, log_quick_filter, log_page_view
    )
    PRODUCTION_MODE = True
    print("✅ Production features enabled (PostgreSQL logging)")
except ImportError as e:
    PRODUCTION_MODE = False
    print(f"⚠️  Production features disabled: {e}")
    print("   Running in development mode (no database)")
```

**3. แก้ secret_key (บรรทัด 12):**

```python
# แทนที่:
# server.secret_key = "your_secret_key"

# ด้วย:
if PRODUCTION_MODE:
    config = get_config()
    server.config.from_object(config)
    server.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    server.secret_key = "dev-secret-key"
```

**4. Initialize database (หลัง login_manager setup, บรรทัด 15):**

```python
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# Initialize database (if available)
if PRODUCTION_MODE and get_config().DATABASE_URL:
    try:
        init_db(server)
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database init failed: {e}")
        PRODUCTION_MODE = False
```

**5. แก้ User class (บรรทัด 17-30):**

```python
# ถ้า PRODUCTION_MODE = True ใช้ database
if PRODUCTION_MODE:
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
else:
    # Development mode: hardcoded users
    class User(UserMixin):
        def __init__(self, username):
            self.id = username
            self.username = username

    @login_manager.user_loader
    def load_user(username):
        users = {"admin": "admin123", "user": "password"}
        if username in users:
            return User(username)
        return None

    def authenticate(username, password):
        users = {"admin": "admin123", "user": "password"}
        if users.get(username) == password:
            return User(username)
        return None
```

**6. แก้ login route (บรรทัด ~485):**

```python
@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if PRODUCTION_MODE:
            # Database authentication
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password) and user.is_active:
                login_user(user)
                log_login(username, success=True)
                user.last_login = datetime.utcnow()
                db.session.commit()
                return redirect("/dashboard/")
            else:
                log_login(username, success=False)
                return render_template("login.html", error="Invalid credentials")
        else:
            # Development mode
            user = authenticate(username, password)
            if user:
                login_user(user)
                return redirect("/dashboard/")
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")
```

**7. แก้ logout route:**

```python
@server.route("/logout", methods=["POST"])
@login_required
def logout():
    if PRODUCTION_MODE:
        log_logout()
    logout_user()
    return redirect("/login")
```

---

### Phase 2: Add Logging (15 minutes)

**8. Log navigate clicks (ใน update_map callback):**

เพิ่มใน callback ที่มี Navigate button:

```python
# หาส่วนที่สร้าง Navigate link ในตาราง
# เพิ่ม logging เมื่อคลิก (ต้องใช้ client-side callback หรือ log เมื่อ render)

# ตัวอย่าง: log เมื่อแสดงตาราง
if PRODUCTION_MODE and not filtered.empty:
    log_page_view('dashboard_with_data')
```

**9. Log filter changes:**

```python
# ในทุก callback ที่มี filter Input
# เพิ่มบรรทัดนี้ต้นฟังก์ชัน:

if PRODUCTION_MODE:
    if province:
        log_filter_change('province', province)
    if district:
        log_filter_change('district', district)
    # ... etc
```

**10. Log quick filter:**

```python
# ใน callback ที่จัดการ quick filter buttons:

if PRODUCTION_MODE:
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'quick-high-potential':
            log_quick_filter('high_potential')
        elif button_id == 'quick-show-all':
            log_quick_filter('show_all')
```

---

### Phase 3: Add Online Counter (15 minutes)

**11. เพิ่ม counter ใน Navbar:**

แก้ Navbar layout (บรรทัด ~70):

```python
dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H4("🔥 Sales Dashboard", className="text-white mb-0"),
                width="auto"
            ),
            # เพิ่ม online counter
            dbc.Col(
                html.Div(id='online-counter', className="text-white"),
                width="auto"
            ) if PRODUCTION_MODE else None,
            dbc.Col(
                html.A("🚪 Logout", href="/logout", className="btn btn-outline-light btn-sm"),
                width="auto"
            )
        ], align="center", className="w-100 justify-content-between")
    ], fluid=True),
    color="primary",
    dark=True,
    sticky="top"
)
```

**12. เพิ่ม callback update counter:**

```python
if PRODUCTION_MODE:
    @app.callback(
        Output('online-counter', 'children'),
        Input('interval-component', 'n_intervals')  # ต้องเพิ่ม dcc.Interval
    )
    def update_online_counter(n):
        count = get_active_users_count()
        return f"👥 Online: {count}"

    # เพิ่ม Interval component ใน layout
    app.layout.children.append(
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # Update every 30 seconds
            n_intervals=0
        )
    )
```

---

### Phase 4: Add Stats Page (30 minutes)

**13. สร้าง /stats route:**

```python
if PRODUCTION_MODE:
    @server.route("/stats")
    @login_required
    def stats():
        if not current_user.is_admin():
            return "Access denied", 403

        from logger import get_user_stats, get_recent_activity

        stats = get_user_stats(days=30)
        recent = get_recent_activity(limit=50)

        return render_template("stats.html", stats=stats, recent=recent)
```

**14. สร้าง templates/stats.html:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Stats - TOL Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>📊 Usage Statistics</h1>

        <div class="row mt-4">
            <div class="col-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5>Total Events</h5>
                        <h2>{{ stats.total_events }}</h2>
                    </div>
                </div>
            </div>
            <!-- Add more cards here -->
        </div>

        <h3 class="mt-5">Recent Activity</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Time</th>
                    <th>User</th>
                    <th>Event</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {% for log in recent %}
                <tr>
                    <td>{{ log.timestamp }}</td>
                    <td>{{ log.username }}</td>
                    <td>{{ log.event_type }}</td>
                    <td>{{ log.event_data }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <a href="/dashboard/" class="btn btn-primary">Back to Dashboard</a>
    </div>
</body>
</html>
```

---

### Phase 5: Add User Management (45 minutes)

**15. สร้าง /admin/users route:**

```python
if PRODUCTION_MODE:
    @server.route("/admin/users")
    @login_required
    def admin_users():
        if not current_user.is_admin():
            return "Access denied", 403

        users = User.query.all()
        return render_template("admin_users.html", users=users)

    @server.route("/admin/users/create", methods=["POST"])
    @login_required
    def create_user():
        if not current_user.is_admin():
            return "Access denied", 403

        username = request.form.get("username")
        password = request.form.get("password")
        full_name = request.form.get("full_name")
        role = request.form.get("role", "user")

        if User.query.filter_by(username=username).first():
            return "User already exists", 400

        user = User(
            username=username,
            full_name=full_name,
            role=role,
            created_by_id=current_user.id
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect("/admin/users")
```

---

## 🧪 Testing Integration

### Local Testing (with SQLite):

```bash
# Set environment variable
$env:DATABASE_URL="sqlite:///test.db"

# Run app
python app_sales_v2.py

# Check console for:
# ✅ Production features enabled
# ✅ Database initialized
# ✅ Default admin user created
```

### Render Testing:

1. Deploy ตาม DEPLOYMENT.md
2. Check logs ใน Render dashboard
3. Login และทดสอบ features
4. Check /stats page (admin only)

---

## 📊 Expected Results

**หลัง integrate ทั้งหมด:**

1. ✅ Login/Logout → บันทึกใน database
2. ✅ Navigate clicks → บันทึก destination
3. ✅ Filter changes → บันทึก filter selections
4. ✅ Online counter → แสดงจำนวน users
5. ✅ Stats page → แสดง analytics (admin only)
6. ✅ User management → สร้าง/แก้/ลบ users (admin only)

---

## ⚠️ Important Notes

1. **Backup ก่อนแก้:** สำรอง app_sales_v2.py ก่อนทุกครั้ง
2. **Test local ก่อน:** ทดสอบบน local ก่อน deploy
3. **ทีละขั้น:** ทำ Phase 1 ให้ได้ก่อนไป Phase 2
4. **Check logs:** ดู console/logs หาก error
5. **Fallback ทำงาน:** ถ้า database fail ยัง run ได้แบบเดิม

---

## 🔧 Rollback (ถ้ามีปัญหา)

```bash
# ถ้าเกิด error ให้:
# 1. ลบ code ที่เพิ่มออก
# 2. หรือ comment ออกด้วย #
# 3. หรือ restore จาก backup
# 4. app_sales_v2.py จะกลับมาใช้งานได้ปกติ
```

---

## 📞 Need Help?

1. Check error messages ใน console
2. Check Render logs
3. Verify DATABASE_URL is set correctly
4. Make sure all imports work

---

**Last Updated:** 2025-10-05
**Status:** Ready for integration (optional)
**Risk Level:** Low (with backup)
