from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dash import Dash, dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
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
data_path = 'd:/2025/Dash/TOL_Login_Dash/Prepared_True_Dataset_Updated.csv'
data = pd.read_csv(data_path)

# Data Preprocessing
if '%Port_Utilize' not in data.columns:
    data['%Port_Utilize'] = 0.0
else:
    data['%Port_Utilize'] = data['%Port_Utilize'].replace(['-', ' -   ', ' '], np.nan)
    data['%Port_Utilize'] = data['%Port_Utilize'].apply(
        lambda x: str(x).rstrip('%') if isinstance(x, str) else x
    ).apply(pd.to_numeric, errors='coerce')
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

# Calculate Household Density
data['Household Density'] = data['Household'] / 0.25
data['Installation Density'] = data['Install'] / data['Install'].sum()

# Normalize factors
data['Normalized Household Density'] = (data['Household Density'] - data['Household Density'].min()) / (data['Household Density'].max() - data['Household Density'].min())
data['Normalized Installation Density'] = (data['Installation Density'] - data['Installation Density'].min()) / (data['Installation Density'].max() - data['Installation Density'].min())
data['Normalized Net Add'] = (data['Net Add'] - data['Net Add'].min()) / (data['Net Add'].max() - data['Net Add'].min())
data['Normalized Market Share'] = (data['Market Share True (%)'] - data['Market Share True (%)'].min()) / (data['Market Share True (%)'].max() - data['Market Share True (%)'].min())
data['Normalized True Speed'] = (data['True Speed'] - data['True Speed'].min()) / (data['True Speed'].max() - data['True Speed'].min())

# Recalculate Potential Score
data['Potential Score'] = (
    0.4 * data['Normalized Household Density'] +
    0.25 * data['Normalized Installation Density'] +
    0.2 * data['Normalized Net Add'] +
    0.05 * data['Normalized Market Share'] +
    0.1 * data['Normalized True Speed']
) * 100

# Adjust Potential Score to increment by 5%
data['Potential Score'] = (data['Potential Score'] / 5).apply(np.ceil) * 5

# Create Dash App with Bootstrap theme
app = Dash(
    __name__,
    server=server,
    url_base_pathname="/dashboard/",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
app.title = "TOL Sales Journey - Mobile Ready"

# Responsive Layout with DBC
app.layout = dbc.Container([
    # Navbar
    dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.NavbarBrand("🚗 TOL Sales Journey", className="ms-2")
                ], width=8),
                dbc.Col([
                    html.A(
                        dbc.Button("Logout", color="danger", size="sm"),
                        href="/logout"
                    )
                ], width=4, className="text-end")
            ], align="center", className="w-100")
        ], fluid=True),
        color="primary",
        dark=True,
        sticky="top",
        className="mb-3"
    ),

    # Main Content
    dbc.Row([
        # Filters Column
        dbc.Col([
            # Quick Filters Card
            dbc.Card([
                dbc.CardHeader("🎯 Quick Filters", className="fw-bold"),
                dbc.CardBody([
                    dbc.Button(
                        "🔥 High Potential (>70)",
                        id='quick-high-potential',
                        color="success",
                        className="w-100 mb-2",
                        n_clicks=0
                    ),
                    dbc.Button(
                        "📍 Show All",
                        id='quick-show-all',
                        color="primary",
                        className="w-100",
                        n_clicks=0
                    ),
                ])
            ], className="mb-3"),

            # Location Filters Card
            dbc.Card([
                dbc.CardHeader([
                    html.Span("📍 Location Filters", className="fw-bold"),
                    dbc.Button(
                        "▼",
                        id="collapse-location-button",
                        className="float-end",
                        color="link",
                        size="sm",
                        n_clicks=0
                    )
                ]),
                dbc.Collapse([
                    dbc.CardBody([
                        html.Label("Province:"),
                        dcc.Dropdown(
                            id='province-filter',
                            options=[{'label': prov, 'value': prov} for prov in data['Province'].unique()],
                            placeholder="Select Province",
                            className="mb-2"
                        ),
                        html.Label("District:"),
                        dcc.Dropdown(
                            id='district-filter',
                            placeholder="Select District",
                            className="mb-2"
                        ),
                        html.Label("Sub-district:"),
                        dcc.Dropdown(
                            id='subdistrict-filter',
                            placeholder="Select Sub-district",
                            className="mb-2"
                        ),
                        html.Label("Happy Block:"),
                        dcc.Dropdown(
                            id='happyblock-filter',
                            placeholder="Select Happy Block"
                        ),
                    ])
                ], id="collapse-location", is_open=True)
            ], className="mb-3"),

            # Advanced Filters Card
            dbc.Card([
                dbc.CardHeader([
                    html.Span("⚙️ Advanced Filters", className="fw-bold"),
                    dbc.Button(
                        "▼",
                        id="collapse-advanced-button",
                        className="float-end",
                        color="link",
                        size="sm",
                        n_clicks=0
                    )
                ]),
                dbc.Collapse([
                    dbc.CardBody([
                        html.Label("Net Add:", className="small"),
                        dcc.RangeSlider(
                            id='net-add-slider',
                            min=int(data['Net Add'].min()),
                            max=int(data['Net Add'].max()),
                            step=2,
                            marks={i: {'label': str(i), 'style': {'fontSize': '10px'}} for i in range(int(data['Net Add'].min()), int(data['Net Add'].max()) + 1, 4)},
                            value=[int(data['Net Add'].min()), int(data['Net Add'].max())],
                            className="mb-3"
                        ),
                        html.Label("Potential Score:", className="small"),
                        dcc.RangeSlider(
                            id='potential-score-slider',
                            min=int(data['Potential Score'].min()),
                            max=int(data['Potential Score'].max()),
                            step=1,
                            marks={i: {'label': f"{i}", 'style': {'fontSize': '10px'}} for i in range(0, int(data['Potential Score'].max()) + 1, 20)},
                            value=[int(data['Potential Score'].min()), int(data['Potential Score'].max())],
                            className="mb-3"
                        ),
                        html.Label("Port Utilize (%):", className="small"),
                        dcc.RangeSlider(
                            id='port-utilization-slider',
                            min=0, max=100, step=1,
                            marks={i: {'label': f"{i}%", 'style': {'fontSize': '10px'}} for i in range(0, 101, 25)},
                            value=[0, 100],
                            className="mb-3"
                        ),
                        html.Label("Market Share True (%):", className="small"),
                        dcc.RangeSlider(
                            id='market-share-true-slider',
                            min=0, max=100, step=1,
                            marks={i: {'label': f"{i}%", 'style': {'fontSize': '10px'}} for i in range(0, 101, 25)},
                            value=[0, 100],
                            className="mb-3"
                        ),
                        html.Label("L2 Aging (months):", className="small"),
                        dcc.RangeSlider(
                            id='l2-aging-slider',
                            min=0,
                            max=data['L2_Aging_Months'].max(),
                            step=1,
                            marks={i: {'label': f"{i}", 'style': {'fontSize': '10px'}} for i in range(0, int(data['L2_Aging_Months'].max()) + 1, 24)},
                            value=[0, int(data['L2_Aging_Months'].max())]
                        ),
                    ])
                ], id="collapse-advanced", is_open=False)
            ])
        ], xs=12, sm=12, md=4, lg=3, className="mb-3"),

        # Map & Table Column
        dbc.Col([
            # Map Card
            dbc.Card([
                dbc.CardHeader(id="map-header", className="fw-bold"),
                dbc.CardBody([
                    dcc.Graph(
                        id='map',
                        config={'scrollZoom': True, 'displayModeBar': True},
                        style={'height': '500px'}
                    )
                ], className="p-1")
            ], className="mb-3"),

            # Table Card
            dbc.Card([
                dbc.CardHeader("📋 Target Locations", className="fw-bold"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='location-table',
                        columns=[
                            {'name': '🎯 Score', 'id': 'Potential Score', 'type': 'numeric'},
                            {'name': '📍 Sub-district', 'id': 'Sub-district'},
                            {'name': '🏘️ Block', 'id': 'Happy Block'},
                            {'name': '📶 Use', 'id': 'Port Use', 'type': 'numeric'},
                            {'name': '✅ Avail', 'id': 'Port Available', 'type': 'numeric'},
                            {'name': '🗺️ Nav', 'id': 'Navigate', 'presentation': 'markdown'},
                        ],
                        data=[],
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '8px',
                            'fontSize': '13px',
                            'minWidth': '80px'
                        },
                        style_header={
                            'backgroundColor': '#0d6efd',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'fontSize': '12px'
                        },
                        style_data_conditional=[
                            {
                                'if': {'filter_query': '{Potential Score} >= 70'},
                                'backgroundColor': '#d1e7dd',
                                'color': '#0f5132'
                            },
                            {
                                'if': {'filter_query': '{Potential Score} >= 50 && {Potential Score} < 70'},
                                'backgroundColor': '#fff3cd',
                                'color': '#664d03'
                            },
                            {
                                'if': {'filter_query': '{Potential Score} < 50'},
                                'backgroundColor': '#f8d7da',
                                'color': '#842029'
                            }
                        ],
                        sort_action='native',
                        page_size=10,
                        page_action='native'
                    )
                ], className="p-2")
            ])
        ], xs=12, sm=12, md=8, lg=9)
    ])
], fluid=True, className="px-2 px-md-4")

# Callbacks
@app.callback(
    Output('collapse-location', 'is_open'),
    Input('collapse-location-button', 'n_clicks'),
    State('collapse-location', 'is_open')
)
def toggle_location_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('collapse-advanced', 'is_open'),
    Input('collapse-advanced-button', 'n_clicks'),
    State('collapse-advanced', 'is_open')
)
def toggle_advanced_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

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
    return [
        {'label': subdist, 'value': subdist}
        for subdist in filtered['Sub-district'].unique()
        if subdist is not None and isinstance(subdist, str) and subdist.strip() != ""
    ]

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
    [Output('map', 'figure'),
     Output('potential-score-slider', 'value'),
     Output('location-table', 'data'),
     Output('map-header', 'children')],
    [Input('province-filter', 'value'),
     Input('district-filter', 'value'),
     Input('subdistrict-filter', 'value'),
     Input('happyblock-filter', 'value'),
     Input('net-add-slider', 'value'),
     Input('potential-score-slider', 'value'),
     Input('port-utilization-slider', 'value'),
     Input('market-share-true-slider', 'value'),
     Input('l2-aging-slider', 'value'),
     Input('quick-high-potential', 'n_clicks'),
     Input('quick-show-all', 'n_clicks')]
)
def update_map(province, district, subdistrict, happy_block, net_add_range, potential_score_range, port_util_range, market_share_true_range, l2_aging_range, high_potential_clicks, show_all_clicks):
    from dash import callback_context
    ctx = callback_context

    # Handle Quick Filter buttons
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'quick-high-potential':
            potential_score_range = [70, 100]
        elif button_id == 'quick-show-all':
            potential_score_range = [int(data['Potential Score'].min()), int(data['Potential Score'].max())]

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
        empty_fig = {
            "data": [],
            "layout": {
                "title": "No data available",
                "mapbox": {"style": "open-street-map", "center": {"lat": 8.5, "lon": 100}, "zoom": 6},
            },
        }
        return empty_fig, potential_score_range, [], "📍 No locations found"

    # Calculate center
    center_lat = filtered['Latitude'].mean()
    center_lon = filtered['Longitude'].mean()

    fig = px.scatter_mapbox(
        filtered,
        lat="Latitude",
        lon="Longitude",
        size="Port Use",
        color="Potential Score",
        hover_name="Sub-district",
        hover_data={
            "Latitude": False,
            "Longitude": False,
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
            "Potential Score": True,
        },
        color_continuous_scale="YlGn",  # เขียวเข้ม (High) → เหลือง (Low)
        zoom=10
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        dragmode='pan',
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lon)
        )
    )

    # Prepare table data
    table_data = filtered.sort_values('Potential Score', ascending=False).copy()
    table_data['Navigate'] = table_data.apply(
        lambda row: f"[🗺️]( https://www.google.com/maps/dir/?api=1&destination={row['Latitude']},{row['Longitude']})",
        axis=1
    )

    table_columns = ['Potential Score', 'Sub-district', 'Happy Block', 'Port Use', 'Port Available', 'Navigate']
    table_dict = table_data[table_columns].to_dict('records')

    header_text = f"📍 {len(filtered)} locations | Avg Score: {filtered['Potential Score'].mean():.1f}"

    return fig, potential_score_range, table_dict, header_text

# Flask Routes
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
    app.run(debug=True, host='0.0.0.0', port=8051)
