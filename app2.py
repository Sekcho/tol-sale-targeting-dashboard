from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Flask server setup
server = Flask(__name__)
server.secret_key = "your_secret_key"

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# User Authentication Setup
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Predefined users
users = {
    "admin": User(1, "admin", "admin123"),
    "user": User(2, "user", "password")
}

@login_manager.user_loader
def load_user(user_id):
    return next((u for u in users.values() if str(u.id) == user_id), None)

def authenticate(username, password):
    user = users.get(username)
    if user and user.password == password:
        return user
    return None

# Load Dataset
data_path = 'd:/2025/Dash/TOL_Dass/Prepared_True_Dataset_Updated.csv'
data = pd.read_csv(data_path)

# Data Preprocessing
if '%Port_Utilize' not in data.columns:
    data['%Port_Utilize'] = 0.0
else:
    data['%Port_Utilize'] = data['%Port_Utilize'].replace(['-', ' -   ', ' '], np.nan)
    data['%Port_Utilize'] = data['%Port_Utilize'].str.rstrip('%').apply(pd.to_numeric, errors='coerce')
    data['%Port_Utilize'] = data['%Port_Utilize'].fillna(0)

market_share_cols = ['Market Share True (%)', 'Market Share AIS (%)', 'Market Share 3BB (%)', 'Market Share NT (%)']
for col in market_share_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

data['L2 Inservice date'] = pd.to_datetime(data['L2 Inservice date'], errors='coerce')
current_date = datetime.now()
data['L2_Aging_Months'] = data['L2 Inservice date'].apply(
    lambda x: (current_date.year - x.year) * 12 + (current_date.month - x.month) if pd.notnull(x) else None
)

data['Port Use'] = data['Port Use'].apply(lambda x: max(x, 0) if pd.notnull(x) else 0)
data['Potential Score'] = data['Potential Score'].apply(lambda x: max(x, 0) if pd.notnull(x) else 0)

# Create Dash App
app = Dash(__name__, server=server, url_base_pathname="/dashboard/")
app.title = "TOL Sales Dashboard"

app.layout = html.Div([
    html.H1("TOL Sales Targeting Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Province:"),
        dcc.Dropdown(
            id='province-filter',
            options=[{'label': prov, 'value': prov} for prov in data['Province'].unique()],
            placeholder="Select Province",
        ),
        html.Label("Select District:"),
        dcc.Dropdown(id='district-filter', placeholder="Select District"),
        html.Label("Select Sub-district:"),
        dcc.Dropdown(id='subdistrict-filter', placeholder="Select Sub-district"),
        html.Label("Select Happy Block:"),
        dcc.Dropdown(id='happyblock-filter', placeholder="Select Happy Block"),
        html.Label("Net Add Filter:"),
        dcc.RangeSlider(
            id='net-add-slider',
            min=int(data['Net Add'].min()),
            max=int(data['Net Add'].max()),
            step=1,
            marks={i: str(i) for i in range(int(data['Net Add'].min()), int(data['Net Add'].max()) + 1, 1)},
            value=[int(data['Net Add'].min()), int(data['Net Add'].max())],
        ),
        html.Label("Potential Score Range:"),
        dcc.RangeSlider(
            id='potential-score-slider',
            min=int(data['Potential Score'].min()),
            max=int(data['Potential Score'].max()),
            step=1,
            marks={i: f"{i}" for i in range(int(data['Potential Score'].min()), int(data['Potential Score'].max()) + 1, 10)},
            value=[int(data['Potential Score'].min()), int(data['Potential Score'].max())],
        ),
        html.Label("% Port Utilize Range:"),
        dcc.RangeSlider(
            id='port-utilization-slider',
            min=0, max=100, step=1,
            marks={i: f"{i}%" for i in range(0, 101, 10)},
            value=[0, 100],
        ),
        html.Label("Market Share True (%):"),
        dcc.RangeSlider(
            id='market-share-true-slider',
            min=0,
            max=100,
            step=1,
            marks={i: f"{i}%" for i in range(0, 101, 10)},
            value=[0, 100],
        ),
        html.Label("L2 Aging:"),
        dcc.RangeSlider(
            id='l2-aging-slider',
            min=0,
            max=data['L2_Aging_Months'].max(),
            step=1,
            marks={i: f"{i}" for i in range(0, int(data['L2_Aging_Months'].max()) + 1, 12)},
            value=[0, int(data['L2_Aging_Months'].max())],
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    dcc.Graph(
        id='map',
        style={'width': '65%', 'height': '800px', 'display': 'inline-block'},
        config={
            'scrollZoom': True,
            'displayModeBar': True,
        }
    ),
])

@app.callback(
    Output('district-filter', 'options'),
    Input('province-filter', 'value')
)
def update_district_options(selected_province):
    if selected_province:
        filtered = data[data['Province'] == selected_province]
        return [{'label': dist, 'value': dist} for dist in filtered['District'].unique()]
    return []

@app.callback(
    Output('subdistrict-filter', 'options'),
    [Input('province-filter', 'value'), Input('district-filter', 'value')]
)
def update_subdistrict_options(selected_province, selected_district):
    filtered = data.copy()
    if selected_province:
        filtered = filtered[filtered['Province'] == selected_province]
    if selected_district:
        filtered = filtered[filtered['District'] == selected_district]
    return [{'label': subdist, 'value': subdist} for subdist in filtered['Sub-district'].unique()]

@app.callback(
    Output('happyblock-filter', 'options'),
    [Input('province-filter', 'value'), Input('district-filter', 'value'), Input('subdistrict-filter', 'value')]
)
def update_happyblock_options(selected_province, selected_district, selected_subdistrict):
    filtered = data.copy()
    if selected_province:
        filtered = filtered[filtered['Province'] == selected_province]
    if selected_district:
        filtered = filtered[filtered['District'] == selected_district]
    if selected_subdistrict:
        filtered = filtered[filtered['Sub-district'] == selected_subdistrict]
    return [{'label': hb, 'value': hb} for hb in filtered['Happy Block'].unique()]

@app.callback(
    Output('map', 'figure'),
    [Input('province-filter', 'value'),
     Input('district-filter', 'value'),
     Input('subdistrict-filter', 'value'),
     Input('happyblock-filter', 'value'),
     Input('net-add-slider', 'value'),
     Input('potential-score-slider', 'value'),
     Input('port-utilization-slider', 'value'),
     Input('market-share-true-slider', 'value'),
     Input('l2-aging-slider', 'value')]
)
def update_map(province, district, subdistrict, happy_block, net_add_range, potential_score_range, port_util_range, market_share_true_range, l2_aging_range):
    filtered = data.copy()

    if province:
        filtered = filtered[filtered['Province'] == province]
    if district:
        filtered = filtered[filtered['District'] == district]
    if subdistrict:
        filtered = filtered[filtered['Sub-district'] == subdistrict]
    if happy_block:
        filtered = filtered[filtered['Happy Block'] == happy_block]

    filtered = filtered[
        (filtered['Net Add'] >= net_add_range[0]) &
        (filtered['Net Add'] <= net_add_range[1]) &
        (filtered['Potential Score'] >= potential_score_range[0]) &
        (filtered['Potential Score'] <= potential_score_range[1]) &
        (filtered['%Port_Utilize'] >= port_util_range[0]) &
        (filtered['%Port_Utilize'] <= port_util_range[1]) &
        (filtered['Market Share True (%)'] >= market_share_true_range[0]) &
        (filtered['Market Share True (%)'] <= market_share_true_range[1]) &
        (filtered['L2_Aging_Months'] >= l2_aging_range[0]) &
        (filtered['L2_Aging_Months'] <= l2_aging_range[1])
    ]

    if filtered.empty:
        return {
            "data": [],
            "layout": {
                "title": "No data available",
                "mapbox": {"style": "open-street-map"},
            },
        }

    fig = px.scatter_mapbox(
        filtered,
        lat="Latitude",
        lon="Longitude",
        size="Port Use",
        color="Potential Score",
        hover_name="Sub-district",
        hover_data={
            "Sub-district": True,
            "Household": True,
            "Happy Block": True,
            "L2": True,
            "Port Capacity": True,
            "Port Available": True,
            "Port Use": True,
            "%Port_Utilize": True,
            "Net Add": True,
            "Market Share True (%)": ":.2f",
            "Market Share AIS (%)": ":.2f",
            "Market Share 3BB (%)": ":.2f",
            "Market Share NT (%)": ":.2f",
            "Competitor Speed": True,
            "True Speed": True,
            "L2_Aging_Months": True,
            "Latitude": True,
            "Longitude": True,
        },
        color_continuous_scale="Viridis",
        title="Potential Score and Sales Insights",
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": filtered["Latitude"].mean(), "lon": filtered["Longitude"].mean()},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision=True
    )
    return fig

@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = authenticate(username, password)
        if user:
            login_user(user)
            return redirect("/dashboard/")
        return "Invalid credentials", 401
    return render_template("login.html")

@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@server.before_request
def restrict_dashboard():
    if request.path.startswith("/dashboard") and not current_user.is_authenticated:
        return redirect("/login")

if __name__ == "__main__":
    app.run_server(debug=True)
