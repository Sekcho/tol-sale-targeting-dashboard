# Development Guide

คู่มือสำหรับนักพัฒนาที่ต้องการพัฒนาต่อยอด project นี้

## สารบัญ
1. [Architecture](#architecture)
2. [Code Structure](#code-structure)
3. [Data Flow](#data-flow)
4. [Adding Features](#adding-features)
5. [Testing](#testing)
6. [Best Practices](#best-practices)

---

## Architecture

### System Overview
```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│    Flask    │ ◄─── Login/Logout
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Dash     │ ◄─── Dashboard UI
│     App     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Plotly    │ ◄─── Map Visualization
│   Mapbox    │
└─────────────┘
```

### Tech Stack Details

**Backend:**
- Flask 3.0.3 - Web server
- Flask-Login 0.6.3 - Authentication

**Frontend:**
- Dash 2.18.2 - Web framework
- Plotly 5.24.1 - Visualization
- dash_table - Data tables

**Data Processing:**
- Pandas 2.2.3 - Data manipulation
- NumPy 2.2.2 - Numerical operations

---

## Code Structure

### app.py / app_sales.py

```python
# 1. Imports
from flask import Flask, ...
from dash import Dash, dcc, html, ...

# 2. Flask Setup
server = Flask(__name__)
login_manager = LoginManager()

# 3. User Authentication
class User(UserMixin): ...
def authenticate(): ...

# 4. Data Loading & Preprocessing
data = pd.read_csv(...)
# Potential Score calculation
# Data cleaning

# 5. Dash App Setup
app = Dash(__name__, server=server, ...)

# 6. Layout
app.layout = html.Div([
    # Header
    # Filters
    # Map
    # Table (app_sales.py only)
])

# 7. Callbacks
@app.callback(...)
def update_district_options(): ...

@app.callback(...)
def update_map(): ...

# 8. Flask Routes
@server.route("/login", ...)
def login(): ...

@server.route("/logout", ...)
def logout(): ...

# 9. Run
if __name__ == "__main__":
    app.run(debug=True)
```

---

## Data Flow

### 1. User Login Flow
```
User → /login → authenticate() → Flask-Login → /dashboard/
```

### 2. Map Update Flow
```
User selects filter
    ↓
Callback triggered
    ↓
Filter data (Pandas)
    ↓
Calculate center (mean Lat/Lon)
    ↓
Create scatter_mapbox (Plotly)
    ↓
Update layout
    ↓
Return figure to browser
```

### 3. Table Update Flow (app_sales.py)
```
User selects filter
    ↓
Same as Map Update
    ↓
Sort by Potential Score
    ↓
Add Navigate column
    ↓
Convert to dict
    ↓
Return to DataTable
```

---

## Adding Features

### 1. เพิ่ม Filter ใหม่

**Example: เพิ่ม "Province Type" filter**

```python
# Step 1: เพิ่มใน layout
html.Label("Province Type:"),
dcc.Dropdown(
    id='province-type-filter',
    options=[
        {'label': 'Central', 'value': 'central'},
        {'label': 'North', 'value': 'north'},
        {'label': 'South', 'value': 'south'}
    ],
    placeholder="Select Province Type"
),

# Step 2: เพิ่ม Input ใน callback
@app.callback(
    Output('map', 'figure'),
    [Input('province-type-filter', 'value'),  # ← เพิ่มบรรทัดนี้
     Input('province-filter', 'value'),
     ...]
)
def update_map(province_type, province, ...):  # ← เพิ่ม parameter
    filtered = data.copy()

    # Step 3: Apply filter
    if province_type:
        province_map = {
            'central': ['Bangkok', 'Nonthaburi', ...],
            'north': ['Chiang Mai', ...],
            'south': ['Phuket', 'Surat Thani', ...]
        }
        filtered = filtered[filtered['Province'].isin(province_map[province_type])]

    # ... rest of code
```

### 2. เพิ่มคอลัมน์ใหม่ใน Table

```python
# Step 1: เพิ่มใน columns
columns=[
    {'name': '🎯 Potential', 'id': 'Potential Score'},
    {'name': '🆕 New Column', 'id': 'NewColumn'},  # ← เพิ่ม
    ...
],

# Step 2: เพิ่มในการเตรียมข้อมูล
table_columns = [
    'Potential Score',
    'NewColumn',  # ← เพิ่ม
    'Sub-district',
    ...
]
```

### 3. เพิ่ม Callback ใหม่

```python
@app.callback(
    Output('new-component', 'children'),
    Input('some-filter', 'value')
)
def update_new_component(filter_value):
    # Your logic here
    return "Updated content"
```

---

## Testing

### Manual Testing Checklist

**Login System:**
- [ ] Login with correct credentials
- [ ] Login with wrong credentials
- [ ] Logout
- [ ] Access /dashboard/ without login (should redirect)

**Filters:**
- [ ] Province → District → Sub-district cascade
- [ ] Quick Filter "High Potential"
- [ ] Quick Filter "Show All"
- [ ] All range sliders

**Map:**
- [ ] Zoom in/out with mouse wheel
- [ ] Pan with mouse drag
- [ ] Hover shows correct info
- [ ] Center adjusts when filter changes

**Table (app_sales.py):**
- [ ] Sort by column
- [ ] Pagination works
- [ ] Navigate button opens Google Maps
- [ ] Color coding correct

### Unit Testing (Future)

```python
# tests/test_data.py
def test_potential_score_calculation():
    # Test Potential Score formula
    pass

def test_data_filtering():
    # Test filter logic
    pass

# tests/test_callbacks.py
def test_district_filter_callback():
    # Test cascade filter
    pass
```

---

## Best Practices

### 1. Code Style

**ใช้ PEP 8:**
```python
# Good
def calculate_score(household, install, net_add):
    return (0.4 * household + 0.25 * install + 0.2 * net_add) * 100

# Bad
def calculateScore(household,install,net_add):
    return (0.4*household+0.25*install+0.2*net_add)*100
```

**ใช้ Type Hints:**
```python
from typing import List, Dict

def filter_data(data: pd.DataFrame, province: str) -> pd.DataFrame:
    return data[data['Province'] == province]
```

### 2. Data Processing

**ใช้ .copy() เสมอ:**
```python
# Good - ป้องกัน SettingWithCopyWarning
filtered = data.copy()
filtered['New Column'] = ...

# Bad
filtered = data
filtered['New Column'] = ...  # อาจมี warning
```

**Check empty data:**
```python
if filtered.empty:
    return empty_figure, [], []
```

### 3. Callbacks

**ใช้ Pattern Matching:**
```python
from dash import callback_context

ctx = callback_context
if ctx.triggered:
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'quick-high-potential':
        # Handle high potential
```

**Return tuple ตาม Output order:**
```python
@app.callback(
    [Output('map', 'figure'),
     Output('table', 'data'),
     Output('slider', 'value')],
    ...
)
def callback(...):
    return figure, table_data, slider_value  # ต้องเรียงตาม Output
```

### 4. Performance

**Filter ก่อน loop:**
```python
# Good
filtered = data[data['Province'] == province]
for _, row in filtered.iterrows():
    ...

# Bad
for _, row in data.iterrows():
    if row['Province'] == province:
        ...
```

**ใช้ vectorized operations:**
```python
# Good
data['New'] = data['A'] + data['B']

# Bad
data['New'] = data.apply(lambda row: row['A'] + row['B'], axis=1)
```

---

## Common Issues & Solutions

### 1. Callback ไม่ทำงาน

**สาเหตุ:**
- Output/Input id ผิด
- Missing Input
- Return value ไม่ตรงกับ Output

**วิธีแก้:**
```python
# ตรวจสอบ id ใน layout
html.Div(id='my-div')  # ← ต้องตรงกับ callback

@app.callback(
    Output('my-div', 'children'),  # ← id ตรงกัน
    Input('my-button', 'n_clicks')
)
```

### 2. Map ไม่แสดง

**สาเหตุ:**
- ข้อมูล Lat/Lon เป็น NaN
- Filter กรองข้อมูลหมดทั้งหมด

**วิธีแก้:**
```python
# Check data
print(filtered[['Latitude', 'Longitude']].describe())

# Check empty
if filtered.empty:
    return empty_figure
```

### 3. Performance ช้า

**สาเหตุ:**
- ข้อมูลเยอะเกินไป (>10,000 rows)
- Loop มากเกินไป

**วิธีแก้:**
```python
# 1. ใช้ pagination
page_size=100

# 2. ใช้ clustering
# https://plotly.com/python/map-clustering/

# 3. Downsample data
if len(filtered) > 5000:
    filtered = filtered.sample(5000)
```

---

## Git Workflow

### Branch Strategy

```
main
 ├── develop
 │    ├── feature/new-filter
 │    ├── feature/route-planning
 │    └── bugfix/map-zoom
 └── hotfix/login-error
```

### Commit Message Format

```
<type>: <subject>

<body>

Types:
- feat: ฟีเจอร์ใหม่
- fix: แก้ bug
- docs: เอกสาร
- style: format code
- refactor: ปรับโครงสร้าง
- test: test
- chore: งานเบ็ดเตล็ด

Example:
feat: add radius search filter

- Add radius dropdown (5km/10km/20km)
- Calculate distance from current location
- Update map center
```

---

## Deployment

### Production Checklist

- [ ] Set `debug=False`
- [ ] Change `secret_key` to secure random string
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS
- [ ] Configure CORS if needed
- [ ] Set up logging
- [ ] Add error handling

### Example Production Config

```python
import os

server.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)
```

---

**Questions?** Contact: [Your Email]

**Last Updated:** 2025-10-05
