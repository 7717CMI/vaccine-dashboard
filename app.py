import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random

# Initialize Dash app with modern theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
        {"name": "description", "content": "Global Vaccine Market Analytics Dashboard"},
        {"name": "author", "content": "HealthData AI"}
    ]
)
server = app.server

# Generate comprehensive vaccine market data based on Data-Vaccine.xlsx structure
def generate_comprehensive_data():
    """Generate vaccine market data matching Excel file structure"""
    
    np.random.seed(42)
    years = list(range(2021, 2036))
    regions = ["North America", "Europe", "APAC", "Latin America", "Middle East", "Africa"]
    
    # Diseases/Markets from actual Excel data
    diseases = ["HBV", "Herpes", "TCV", "HPV", "Influenza", "Pneumococcal", "MMR", "Rotavirus", 
                "Meningococcal", "Varicella"]
    
    # Brands by disease (from actual data + extensions)
    brand_map = {
        "HBV": ["Engerix-B", "Heplisav-B", "Recombivax HB", "Twinrix"],
        "Herpes": ["Shingrix", "Zostavax"],
        "TCV": ["Typbar TCV", "Typhim Vi", "Vivotif"],
        "HPV": ["Gardasil 9", "Cervarix"],
        "Influenza": ["Fluzone", "Flucelvax", "FluMist", "Fluad"],
        "Pneumococcal": ["Prevnar 13", "Prevnar 20", "Pneumovax 23", "Synflorix"],
        "MMR": ["M-M-R II", "Priorix"],
        "Rotavirus": ["RotaTeq", "Rotarix"],
        "Meningococcal": ["Bexsero", "Trumenba", "MenACWY"],
        "Varicella": ["Varivax", "ProQuad"]
    }
    
    # Companies
    companies = ["Pfizer", "GSK", "Merck", "Sanofi", "AstraZeneca", "Moderna", "Bharat Biotech", 
                 "Serum Institute"]
    
    # Income classification with countries (from Excel structure)
    country_income_map = {
        "North America": {
            "USA": "High Income", "Canada": "High Income", "Mexico": "Middle Income"
        },
        "Europe": {
            "Germany": "High Income", "UK": "High Income", "France": "High Income", 
            "Spain": "High Income", "Italy": "High Income", "Poland": "Middle Income",
            "Romania": "Middle Income"
        },
        "APAC": {
            "Japan": "High Income", "Australia": "High Income", "Singapore": "High Income",
            "China": "Middle Income", "India": "Middle Income", "Thailand": "Middle Income",
            "Pakistan": "Low Income", "Bangladesh": "Low Income", "Nepal": "Low Income"
        },
        "Latin America": {
            "Brazil": "Middle Income", "Argentina": "Middle Income", "Chile": "Middle Income", 
            "Colombia": "Middle Income", "Peru": "Middle Income"
        },
        "Middle East": {
            "UAE": "High Income", "Saudi Arabia": "High Income", "Israel": "High Income", 
            "Egypt": "Middle Income", "Iraq": "Middle Income"
        },
        "Africa": {
            "South Africa": "Middle Income", "Nigeria": "Low Income", "Kenya": "Low Income", 
            "Ethiopia": "Low Income", "Ghana": "Low Income"
        }
    }
    
    # Additional fields from Excel
    age_groups = ["Pediatric", "Adult", "Elderly", "All Ages"]
    genders = ["Male", "Female", "All"]
    segments = ["Gender", "Brand", "Age", "ROA", "FDF"]
    roa_types = ["IM", "SC", "Oral", "Intranasal"]  # IM from Excel
    fdf_types = ["Vial", "Prefilled Syringe", "Multi-dose Vial", "Oral Solution"]
    procurement_types = ["UNICEF", "GAVI", "PAHO", "Hospital", "Private Clinic", "Government"]
    
    data = []
    record_id = 100000
    
    for year in years:
        for region in regions:
            for country, income_type in country_income_map[region].items():
                for disease in diseases:
                    brands = brand_map[disease]
                    for brand in brands:
                        for age_group in age_groups:
                            for gender in ["Male", "Female"]:
                                # Base values with variation
                                prevalence = random.randint(10000, 500000) * (1 + (year - 2021) * 0.05)
                                incidence = random.randint(20000, 800000) * (1 + (year - 2021) * 0.03)
                                vaccination_rate = random.uniform(5, 95)
                                price = random.uniform(2, 150)
                                price_elasticity = random.uniform(5, 50)
                                volume_units = random.randint(1000, 2000000)
                                revenue = price * volume_units
                                market_value_usd = revenue * random.uniform(0.8, 1.2)
                                market_share_pct = random.uniform(1, 25)
                                cagr = random.uniform(-2, 15)
                                yoy_growth = random.uniform(-5, 20)
                                qty = random.randint(100, 100000)
                                
                                roa = random.choice(roa_types)
                                fdf = random.choice(fdf_types)
                                procurement = random.choice(procurement_types)
                                segment_by = random.choice(["male", "female", brand, age_group])
                                
                                record = {
                                    "record_id": record_id,
                                    "year": year,
                                    "region": region,
                                    "country": country,
                                    "income_type": income_type,
                                    "disease": disease,
                                    "market": disease,  # Same as disease
                                    "brand": brand,
                                    "company": random.choice(companies),
                                    "age_group": age_group,
                                    "gender": gender,
                                    "segment": random.choice(segments),
                                    "segment_by": segment_by,
                                    "roa": roa,
                                    "fdf": fdf,
                                    "formulation": fdf,  # Alias
                                    "procurement": procurement,
                                    "public_private": "Public" if procurement in ["UNICEF", "GAVI", "PAHO", "Government"] else "Private",
                                    # Epidemiology metrics
                                    "prevalence": int(prevalence),
                                    "incidence": int(incidence),
                                    # Vaccination metrics
                                    "vaccination_rate": round(vaccination_rate, 2),
                                    "coverage_rate": round(vaccination_rate * random.uniform(0.8, 1.1), 2),
                                    # Pricing metrics
                                    "price": round(price, 2),
                                    "price_elasticity": round(price_elasticity, 2),
                                    "price_class": "Premium" if price > 50 else ("Standard" if price > 20 else "Budget"),
                                    # Volume and Value metrics
                                    "volume_units": int(volume_units),
                                    "qty": int(qty),
                                    "revenue": round(revenue, 2),
                                    "market_value_usd": round(market_value_usd, 2),
                                    "value": round(market_value_usd, 2),  # Alias
                                    # Market share metrics
                                    "market_share_pct": round(market_share_pct, 2),
                                    "share": round(market_share_pct, 2),  # Alias
                                    # Growth metrics
                                    "cagr": round(cagr, 2),
                                    "yoy_growth": round(yoy_growth, 2),
                                    "yoy": round(yoy_growth, 2),  # Alias
                                    # Additional metrics
                                    "efficacy_pct": round(random.uniform(60, 98), 2),
                                }
                                
                                data.append(record)
                                record_id += 1
    
    df = pd.DataFrame(data)
    return df

# Lazy data generation - only generate on first access
_df_cache = None

def get_data():
    """Lazy load data - generate only once when first accessed"""
    global _df_cache
    if _df_cache is None:
        print("[INFO] Generating vaccine market data...")
        _df_cache = generate_comprehensive_data()
        print(f"[OK] Generated {len(_df_cache):,} records")
    return _df_cache

# Quick startup - data will be generated on first page load
print("=" * 60)
print("[START] Dashboard Initializing - Ready for HTTP requests")
print("[INFO] Data will be generated on first page access")
print("=" * 60)


# Main Layout with URL routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Landing Page Layout - Updated with actual Excel sheet names
def landing_page():
    return html.Div([
        # Header
        html.Div([
            html.H1("Global Vaccine Market Analytics Dashboard", className="main-title"),
            html.P("Comprehensive market intelligence and forecasting analysis | 2021-2035", 
                   className="main-subtitle")
        ], className="main-header"),
        
        # Demo Notice
        html.Div([
            "⚠ Demo Dataset • For Illustration Purposes Only • No Real-World Data Association"
        ], className="demo-notice"),
        
        # Landing Container
        html.Div([
            html.H2("Select Analysis Module", className="landing-title"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="EP"),
                        html.Div("Epidemiology", className="analysis-name"),
                        html.P("Disease prevalence and incidence analysis", className="analysis-desc")
                    ], className="analysis-button", id="btn-epidemiology")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4"),
                
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="VR"),
                        html.Div("Vaccination Rate", className="analysis-name"),
                        html.P("Coverage and vaccination rate tracking", className="analysis-desc")
                    ], className="analysis-button", id="btn-vaccination-rate")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4"),
                
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="PR"),
                        html.Div("Pricing Analysis", className="analysis-name"),
                        html.P("Price trends and elasticity insights", className="analysis-desc")
                    ], className="analysis-button", id="btn-pricing")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4"),
                
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="CG"),
                        html.Div("CAGR Analysis", className="analysis-name"),
                        html.P("Growth rates by segments", className="analysis-desc")
                    ], className="analysis-button", id="btn-cagr")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4")
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="MC"),
                        html.Div("MSA Comparison", className="analysis-name"),
                        html.P("Market share comparative analysis", className="analysis-desc")
                    ], className="analysis-button", id="btn-msa-comparison")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4"),
                
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="PC"),
                        html.Div("Procurement Analysis", className="analysis-name"),
                        html.P("Public and private procurement tracking", className="analysis-desc")
                    ], className="analysis-button", id="btn-procurement")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4"),
                
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "#004AAD",
                            "fontWeight": "700"
                        }, children="BD"),
                        html.Div("Brand-Demographic", className="analysis-name"),
                        html.P("Brand performance by demographics", className="analysis-desc")
                    ], className="analysis-button", id="btn-brand-demographic")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4"),
                
                dbc.Col([
                    html.Div([
                        html.Div(className="icon-placeholder", style={
                            "width": "64px", "height": "64px", "margin": "0 auto 16px",
                            "background": "linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%)",
                            "borderRadius": "12px", "display": "flex", "alignItems": "center",
                            "justifyContent": "center", "fontSize": "28px", "color": "white",
                            "fontWeight": "700"
                        }, children="FD"),
                        html.Div("FDF Analysis", className="analysis-name"),
                        html.P("Formulation and ROA performance", className="analysis-desc")
                    ], className="analysis-button", id="btn-fdf")
                ], lg=3, md=4, sm=6, xs=12, className="mb-4")
            ])
        ], className="landing-container"),
        
        # Footer
        html.Div([
            "© 2025 Global Vaccine Market Intelligence | ",
            html.Strong("Powered by HealthData AI"),
            html.Br(),
            html.Small("Demo Data Only • Not for Clinical Use • Enterprise Analytics Platform")
        ], className="footer")
    ])

# Callback for navigation
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    df = get_data()  # Lazy load data on first access
    if pathname == '/epidemiology':
        from pages import epidemiology_page
        return epidemiology_page(df)
    elif pathname == '/vaccination-rate':
        from pages import vaccination_rate_page
        return vaccination_rate_page(df)
    elif pathname == '/pricing':
        from pages import pricing_page
        return pricing_page(df)
    elif pathname == '/cagr':
        from pages import cagr_page
        return cagr_page(df)
    elif pathname == '/msa-comparison':
        from pages import msa_comparison_page
        return msa_comparison_page(df)
    elif pathname == '/procurement':
        from pages import procurement_page
        return procurement_page(df)
    elif pathname == '/brand-demographic':
        from pages import brand_demographic_page
        return brand_demographic_page(df)
    elif pathname == '/fdf':
        from pages import fdf_page
        return fdf_page(df)
    else:
        return landing_page()

# Navigation callbacks for buttons
@app.callback(Output('url', 'pathname'),
              [Input('btn-epidemiology', 'n_clicks'),
               Input('btn-vaccination-rate', 'n_clicks'),
               Input('btn-pricing', 'n_clicks'),
               Input('btn-cagr', 'n_clicks'),
               Input('btn-msa-comparison', 'n_clicks'),
               Input('btn-procurement', 'n_clicks'),
               Input('btn-brand-demographic', 'n_clicks'),
               Input('btn-fdf', 'n_clicks')])
def navigate_to_page(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '/'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    navigation_map = {
        'btn-epidemiology': '/epidemiology',
        'btn-vaccination-rate': '/vaccination-rate',
        'btn-pricing': '/pricing',
        'btn-cagr': '/cagr',
        'btn-msa-comparison': '/msa-comparison',
        'btn-procurement': '/procurement',
        'btn-brand-demographic': '/brand-demographic',
        'btn-fdf': '/fdf'
    }
    
    return navigation_map.get(button_id, '/')

# Import and register all callbacks
from callbacks import register_all_callbacks
register_all_callbacks(app, get_data)  # Pass the getter function, not the data itself

# Run the app
if __name__ == "__main__":
    print("=" * 60)
    print("[START] Global Vaccine Market Analytics Dashboard")
    print("[INFO] Server starting on http://0.0.0.0:8050")
    print("[INFO] Data will be generated on first page access")
    print("=" * 60)
    app.run_server(debug=True, host="0.0.0.0", port=8050)
