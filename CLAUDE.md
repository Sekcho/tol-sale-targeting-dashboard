# TOL Sales Targeting Dashboard

## Project Overview
Internal sales targeting dashboard for TOL (True Online) built with Flask + Plotly Dash. Shows Happy Block-level sales potential on an interactive map with filters.

## Live Deployment
- **Platform:** Railway
- **URL:** https://tol-web-production.up.railway.app
- **Project name:** `tol_targeting`
- **GitHub repo:** `Sekcho/tol-sale-targeting-dashboard`

## Key Files
- `app_sales_v2.py` — main app (Flask server + Dash layout + all routes)
- `models.py` — SQLAlchemy models (User, PageView, ActivityLog)
- `Prepared_True_Dataset_Updated.csv` — sales data (must be present at project root)
- `railway.toml` — Railway deployment config
- `Procfile` — gunicorn start command
- `requirements.txt` — Python dependencies
- `templates/` — login.html, register.html, admin_stats.html

## Architecture
- **Flask** handles auth routes (`/login`, `/logout`, `/register`, `/admin/stats`)
- **Dash** handles the dashboard UI at `/dashboard/`
- **SQLAlchemy** with PostgreSQL (production) or SQLite fallback (local dev)
- **gunicorn** serves the app: `gunicorn app_sales_v2:server`

## Routes
| Route | Description | Access |
|-------|-------------|--------|
| `/` | Redirect to login or dashboard | public |
| `/login` | Login page | public |
| `/logout` | Logout | authenticated |
| `/dashboard/` | Main Dash map dashboard | authenticated |
| `/register` | Create new user | admin only |
| `/admin/stats` | Usage report & user management | admin only |
| `/health` | Health check for Railway | public |

## Default Users
| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | admin |
| `user` | `password` | user |

## Environment Variables
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Railway) |
| `SECRET_KEY` | Flask session secret key |
| `FLASK_ENV` | `production` or `development` |

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (uses SQLite fallback automatically)
python app_sales_v2.py

# Access at http://localhost:8051/login
```

## Deployment (Railway)
The app auto-deploys from GitHub `main` branch via Railway.
- Push to `main` → Railway triggers redeploy automatically
- Database tables and default users are created on first startup via `init_database()`

## Database Models
- **User** — username, hashed password, role (admin/user)
- **PageView** — tracks page hit counts per route
- **ActivityLog** — logs login, logout, dashboard views per user

## Notes
- Migrated from Render to Railway due to Render's ephemeral filesystem breaking SQLite
- `app.py`, `app1.py`, `app2.py`, `applogin.py` are older versions — `app_sales_v2.py` is the active file
- Data uses Thailand timezone (Asia/Bangkok / UTC+7) throughout
