import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CERULEAN,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

# Expose the server for Gunicorn
server = app.server

# Load the dataset
data = pd.read_csv('Go - Sheet1.csv')

# App title
app.title = "Electricity and CO2 Insights"

# Define app layout
app.layout = dbc.Container([
    # Header with gradient background and inspirational quote
    dbc.Row(
        dbc.Col([
            html.H1("Electricity Production and CO2 Emissions Dashboard", 
                    style={"textAlign": "center", "color": "#FFFFFF", "padding": "10px"}),
            html.P(
                "Exploring the journey towards a sustainable future through data",
                style={"textAlign": "center", "color": "#FFFFFF", "fontStyle": "italic"}
            )
        ], style={"background": "linear-gradient(to right, #4CAF50, #2196F3)", "padding": "20px"})
    ),

    # Metrics cards with tooltips and hover effects
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src="https://img.icons8.com/ios/50/4CAF50/co2.png", style={"height": "40px"}),
                html.H3("Total CO2 Emissions (MtCO2)", style={"color": "#4CAF50", "textAlign": "center"}, id="total-co2"),
                html.P(f"{data['CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2'].sum():,.0f}", 
                       style={"fontSize": "24px", "fontWeight": "bold", "textAlign": "center"}),
            ], className="metric-card shadow", 
            style={"backgroundColor": "#E8F5E9", "borderRadius": "10px", "padding": "20px", "transition": "0.3s"}),
            dbc.Tooltip("Total CO2 emissions from fuel combustion across all countries.", target="total-co2")
        ]),

        dbc.Col([
            html.Div([
                html.Img(src="https://img.icons8.com/ios/50/2196F3/electricity.png", style={"height": "40px"}),
                html.H3("Average Electricity Production (TWh)", style={"color": "#2196F3", "textAlign": "center"}, id="avg-electricity"),
                html.P(f"{data['ELECTRICITY PRODUCTION TWH'].mean():,.1f}", 
                       style={"fontSize": "24px", "fontWeight": "bold", "textAlign": "center"}),
            ], className="metric-card shadow", 
            style={"backgroundColor": "#E3F2FD", "borderRadius": "10px", "padding": "20px", "transition": "0.3s"}),
            dbc.Tooltip("Average electricity production across all countries and years.", target="avg-electricity")
        ]),

        dbc.Col([
            html.Div([
                html.I(className="fas fa-solar-panel", style={"fontSize": "40px", "color": "#FF9800"}),
                html.H3("Average Renewable Share (%)", style={"color": "#FF9800", "textAlign": "center"}, id="avg-renewables"),
                html.P(f"{data['SHARE OF RENEWABLES IN ELECTRICITY PRODUCTION PERC'].mean():.1f}", 
                       style={"fontSize": "24px", "fontWeight": "bold", "textAlign": "center"}),
            ], className="metric-card shadow", 
            style={"backgroundColor": "#FFF3E0", "borderRadius": "10px", "padding": "20px", "transition": "0.3s"}),
            dbc.Tooltip("Average share of renewables in electricity production.", target="avg-renewables")
        ])
    ], style={"marginBottom": "20px", "display": "flex", "justifyContent": "space-around"}),

    # Filters Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Select a Country:"),
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[{"label": country, "value": country} for country in data["COUNTRY"].unique()],
                        value=data["COUNTRY"].unique()[0],
                        clearable=False,
                        style={"marginBottom": "15px"}
                    ),

                    html.Label("Select a Year Range:"),
                    dcc.RangeSlider(
                        id="year-slider",
                        min=data["YEAR"].min(),
                        max=data["YEAR"].max(),
                        step=1,
                        marks={year: str(year) for year in range(data["YEAR"].min(), data["YEAR"].max() + 1, 5)},
                        value=[data["YEAR"].min(), data["YEAR"].max()],
                        tooltip={"placement": "bottom"},
                    )
                ])
            ], style={"marginBottom": "20px"})
        ])
    ]),

    # Tabs Section
    dbc.Tabs([
        dbc.Tab(label="CO2 and Electricity Trends", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="co2-trend"), width=6),
                dbc.Col(dcc.Graph(id="electricity-trend"), width=6)
            ])
        ]),

        dbc.Tab(label="Carbon Intensity", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="carbon-intensity"), width=12)
            ])
        ]),

        dbc.Tab(label="Renewables vs Non-Renewables", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="renewable-comparison"), width=12)
            ])
        ]),

        dbc.Tab(label="Energy Sources", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="renewables-share"), width=12)
            ])
        ]),

        dbc.Tab(label="Consumption vs Production", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="consumption-vs-production"), width=12)
            ])
        ]),

        dbc.Tab(label="Regional CO2 Insights", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="regional-co2"), width=12)
            ])
        ]),

        dbc.Tab(label="Correlation Analysis", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="correlation-heatmap"), width=12)
            ])
        ])
    ], style={"marginBottom": "20px"}),

    # Footer Section
    dbc.Row(
        dbc.Col([
            html.P("Data Source: Global Electricity Dataset", style={"textAlign": "center", "fontSize": "12px"}),
            html.P(
                "Developed by Rethabile Gift", 
                style={"textAlign": "center", "fontSize": "12px", "marginBottom": "0"}
            )
        ])
    )
], fluid=True, style={"fontFamily": "Arial, sans-serif", "maxWidth": "1200px", "margin": "0 auto", "padding": "20px"})

# Callbacks for updating the charts
@app.callback(
    [
        Output("co2-trend", "figure"),
        Output("electricity-trend", "figure"),
        Output("carbon-intensity", "figure"),
        Output("renewable-comparison", "figure"),
        Output("renewables-share", "figure"),
        Output("consumption-vs-production", "figure"),
        Output("regional-co2", "figure"),
        Output("correlation-heatmap", "figure")
    ],
    [Input("country-dropdown", "value"), Input("year-slider", "value")]
)
def update_charts(selected_country, year_range):
    filtered_data = data[(data["COUNTRY"] == selected_country) & (data["YEAR"] >= year_range[0]) & (data["YEAR"] <= year_range[1])]

    # CO2 Emissions Trend
    co2_fig = px.line(
        filtered_data,
        x="YEAR",
        y="CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2",
        title=f"CO2 Emissions Trend for {selected_country}",
        labels={"CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2": "CO2 Emissions (MtCO2)"},
        color_discrete_sequence=["#FF5733"],
        template="plotly_dark"
    )

    # Electricity Production Trend
    electricity_fig = px.line(
        filtered_data,
        x="YEAR",
        y="ELECTRICITY PRODUCTION TWH",
        title=f"Electricity Production Trend for {selected_country}",
        labels={"ELECTRICITY PRODUCTION TWH": "Electricity Production (TWh)"},
        color_discrete_sequence=["#33C3FF"],
        template="plotly_dark"
    )

    # Carbon Intensity
    filtered_data["Carbon Intensity"] = filtered_data["CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2"] / filtered_data["ELECTRICITY PRODUCTION TWH"]
    carbon_intensity_fig = px.line(
        filtered_data,
        x="YEAR",
        y="Carbon Intensity",
        title=f"Carbon Intensity for {selected_country}",
        labels={"Carbon Intensity": "kg CO2 per TWh"},
        color_discrete_sequence=["#4CAF50"]
    )

    # Renewable vs Non-Renewable
    renewable_comparison_fig = px.bar(
        filtered_data,
        x="YEAR",
        y=["SHARE OF RENEWABLES IN ELECTRICITY PRODUCTION PERC", "SHARE OF WIND AND SOLAR IN ELECTRICITY PRODUCTION  PERC"],
        title=f"Renewable vs Non-Renewable for {selected_country}",
        labels={"value": "Percentage", "variable": "Source"},
        barmode="group",
        color_discrete_sequence=["#4CAF50", "#FF9800"]
    )

    # Renewables and Wind/Solar Share Pie Chart
    latest_year_data = filtered_data.iloc[-1]
    pie_fig = px.pie(
        names=["Renewables", "Wind/Solar", "Other"],
        values=[
            latest_year_data["SHARE OF RENEWABLES IN ELECTRICITY PRODUCTION PERC"],
            latest_year_data["SHARE OF WIND AND SOLAR IN ELECTRICITY PRODUCTION  PERC"],
            100 - latest_year_data["SHARE OF RENEWABLES IN ELECTRICITY PRODUCTION PERC"]
        ],
        title=f"Energy Source Share for {selected_country} ({int(latest_year_data['YEAR'])})",
        color_discrete_sequence=["#4CAF50", "#FF9800", "#E91E63"]
    )

    # Consumption vs Production
    consumption_vs_production_fig = px.line(
        filtered_data,
        x="YEAR",
        y=["ELECTRICITY PRODUCTION TWH", "ELECTRICITY DOMESTIC CONSUMPTION TWH"],
        title=f"Electricity Consumption vs Production for {selected_country}",
        labels={"value": "Electricity (TWh)", "variable": "Metric"},
        color_discrete_sequence=["#FF5733", "#33C3FF"],
        template="plotly_dark"
    )

    # Regional CO2 Emissions
    regional_data = data[(data["YEAR"] == latest_year_data["YEAR"])]
    regional_co2_fig = px.bar(
        regional_data,
        x="COUNTRY",
        y="CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2",
        color="REGION",
        title=f"CO2 Emissions by Region ({int(latest_year_data['YEAR'])})",
        labels={"CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2": "CO2 Emissions (MtCO2)"},
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    # Correlation Heatmap
    correlation_fig = px.imshow(
        filtered_data[[
            "CO2 EMISSIONS FROM FUEL COMBUSTION MTCO2", 
            "ELECTRICITY PRODUCTION TWH", 
            "ELECTRICITY DOMESTIC CONSUMPTION TWH"
        ]].corr(),
        title="Correlation Analysis",
        labels={"color": "Correlation Coefficient"},
        color_continuous_scale=px.colors.sequential.Viridis
    )

    return co2_fig, electricity_fig, carbon_intensity_fig, renewable_comparison_fig, pie_fig, consumption_vs_production_fig, regional_co2_fig, correlation_fig

# Run the app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CERULEAN,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

server = app.server  # Required for deployment on Render

# Local development entry point
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)


