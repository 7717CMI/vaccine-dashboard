"""
All page layouts for the dashboard based on Data-Vaccine.xlsx structure
"""
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_filter_row(page_prefix, df, filter_configs):
    """Create a row of filters based on configuration"""
    cols = []
    for config in filter_configs:
        field = config['field']
        label = config['label']
        placeholder = config.get('placeholder', f"Select {label.lower()}...")
        
        # Special handling for year field - need to sort numerically
        if field == 'year':
            options = [{"label": str(int(val)), "value": val} for val in sorted(df[field].unique())]
        else:
            options = [{"label": val, "value": val} for val in sorted(df[field].unique())]
        
        col = dbc.Col([
            html.Label(f"{label}:", className="filter-label"),
            dcc.Dropdown(
                id=f"{page_prefix}-{field}-filter",
                options=options,
                value=None,
                multi=True,
                placeholder=placeholder,
                clearable=True
            )
        ], md=config.get('width', 3))
        cols.append(col)
    
    return dbc.Row(cols, style={"marginBottom": "16px"})

# 1. EPIDEMIOLOGY PAGE
def epidemiology_page(df):
    """Filters: Disease, Region, Country, Income"""
    return html.Div([
        html.Div([
            html.H1("Epidemiology Analysis", className="main-title"),
            html.P("Disease prevalence and incidence trends", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("epi", df, [
                {"field": "year", "label": "Year"},
                {"field": "disease", "label": "Disease"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("epi", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country"}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Total Prevalence", className="kpi-label"),
                    html.H3(id="epi-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Total Incidence", className="kpi-label"),
                    html.H3(id="epi-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top Disease", className="kpi-label"),
                    html.H3(id="epi-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Avg Incidence Rate", className="kpi-label"),
                    html.H3(id="epi-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="epi-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="epi-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="epi-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 2. VACCINATION RATE PAGE
def vaccination_rate_page(df):
    """Filters: Disease, Region, Country, Income"""
    return html.Div([
        html.Div([
            html.H1("Vaccination Rate Analysis", className="main-title"),
            html.P("Coverage and vaccination rate tracking", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("vax", df, [
                {"field": "year", "label": "Year"},
                {"field": "disease", "label": "Disease"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("vax", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country"}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Avg Vaccination Rate", className="kpi-label"),
                    html.H3(id="vax-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Coverage Rate", className="kpi-label"),
                    html.H3(id="vax-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top Performing Region", className="kpi-label"),
                    html.H3(id="vax-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Countries Analyzed", className="kpi-label"),
                    html.H3(id="vax-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="vax-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="vax-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="vax-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 3. PRICING ANALYSIS PAGE
def pricing_page(df):
    """Filters: Market, Region, Country, Brand, Income"""
    return html.Div([
        html.Div([
            html.H1("Pricing Analysis", className="main-title"),
            html.P("Price trends and elasticity insights", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("price", df, [
                {"field": "year", "label": "Year"},
                {"field": "market", "label": "Market"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("price", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country"},
                {"field": "brand", "label": "Brand"},
                {"field": "price_class", "label": "Price Class"}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Avg Price (USD)", className="kpi-label"),
                    html.H3(id="price-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Price Elasticity", className="kpi-label"),
                    html.H3(id="price-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Most Expensive Brand", className="kpi-label"),
                    html.H3(id="price-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Price Range", className="kpi-label"),
                    html.H3(id="price-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="price-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="price-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="price-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 4. CAGR ANALYSIS PAGE
def cagr_page(df):
    """Filters: Market, Region, Country, Segment, Income"""
    return html.Div([
        html.Div([
            html.H1("CAGR Analysis", className="main-title"),
            html.P("Compound annual growth rate by segments", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("cagr", df, [
                {"field": "year", "label": "Year"},
                {"field": "market", "label": "Market"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("cagr", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country"},
                {"field": "segment", "label": "Segment Type"},
                {"field": "gender", "label": "Gender", "width": 2}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Avg CAGR %", className="kpi-label"),
                    html.H3(id="cagr-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Highest Growth Segment", className="kpi-label"),
                    html.H3(id="cagr-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Max CAGR", className="kpi-label"),
                    html.H3(id="cagr-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Min CAGR", className="kpi-label"),
                    html.H3(id="cagr-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="cagr-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="cagr-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="cagr-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 5. MSA COMPARISON PAGE
def msa_comparison_page(df):
    """Filters: Market, Region, Country, Segment, Income"""
    return html.Div([
        html.Div([
            html.H1("Market Share Analysis Comparison", className="main-title"),
            html.P("Comparative analysis of market share metrics", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("msa", df, [
                {"field": "year", "label": "Year"},
                {"field": "market", "label": "Market"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("msa", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country"},
                {"field": "segment", "label": "Segment Type"},
                {"field": "gender", "label": "Gender", "width": 2}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Total Value (USD)", className="kpi-label"),
                    html.H3(id="msa-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Total Volume", className="kpi-label"),
                    html.H3(id="msa-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Market Share %", className="kpi-label"),
                    html.H3(id="msa-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("YoY Growth %", className="kpi-label"),
                    html.H3(id="msa-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="msa-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="msa-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="msa-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 6. PROCUREMENT ANALYSIS PAGE
def procurement_page(df):
    """Filters: Market, Region, Country, Public/Private, Brand, Income"""
    return html.Div([
        html.Div([
            html.H1("Procurement Analysis", className="main-title"),
            html.P("Public and private procurement tracking", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("proc", df, [
                {"field": "year", "label": "Year"},
                {"field": "market", "label": "Market"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("proc", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country"},
                {"field": "public_private", "label": "Public/Private"},
                {"field": "brand", "label": "Brand"}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Total Qty Procured", className="kpi-label"),
                    html.H3(id="proc-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Public %", className="kpi-label"),
                    html.H3(id="proc-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Private %", className="kpi-label"),
                    html.H3(id="proc-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top Procurement Type", className="kpi-label"),
                    html.H3(id="proc-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="proc-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="proc-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="proc-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 7. BRAND-DEMOGRAPHIC ANALYSIS PAGE
def brand_demographic_page(df):
    """Filters: Market, Region, Country, Age, Gender, Brand, Income"""
    return html.Div([
        html.Div([
            html.H1("Brand-Demographic Analysis", className="main-title"),
            html.P("Brand performance across demographic segments", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("brand-demo", df, [
                {"field": "year", "label": "Year"},
                {"field": "market", "label": "Market"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("brand-demo", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country", "width": 2},
                {"field": "age_group", "label": "Age Group", "width": 2},
                {"field": "gender", "label": "Gender", "width": 2},
                {"field": "brand", "label": "Brand"}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Total Revenue (USD)", className="kpi-label"),
                    html.H3(id="brand-demo-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top Brand", className="kpi-label"),
                    html.H3(id="brand-demo-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top Age Group", className="kpi-label"),
                    html.H3(id="brand-demo-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Avg Revenue/Brand", className="kpi-label"),
                    html.H3(id="brand-demo-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="brand-demo-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="brand-demo-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="brand-demo-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])

# 8. FDF ANALYSIS PAGE
def fdf_page(df):
    """Filters: Market, Region, Country, Brand, FDF, ROA, Income"""
    return html.Div([
        html.Div([
            html.H1("FDF (Formulation) Analysis", className="main-title"),
            html.P("Formulation and Route of Administration analysis", className="main-subtitle")
        ], className="main-header"),
        
        html.Div([dcc.Link(html.Button("← Back to Home", className="back-btn"), href="/")], 
                 style={"padding": "20px"}),
        
        html.Div([
            html.H2("Filters", className="filters-title"),
            create_filter_row("fdf", df, [
                {"field": "year", "label": "Year"},
                {"field": "market", "label": "Market"},
                {"field": "region", "label": "Region"}
            ]),
            create_filter_row("fdf", df, [
                {"field": "income_type", "label": "Income Type"},
                {"field": "country", "label": "Country", "width": 2},
                {"field": "brand", "label": "Brand", "width": 2},
                {"field": "fdf", "label": "FDF", "width": 2},
                {"field": "roa", "label": "ROA"}
            ])
        ], className="filters-container"),
        
        # KPI Cards
        html.Div([
            dbc.Row([
                dbc.Col([html.Div([
                    html.P("Total Revenue (USD)", className="kpi-label"),
                    html.H3(id="fdf-kpi-1", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top FDF Type", className="kpi-label"),
                    html.H3(id="fdf-kpi-2", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Top ROA", className="kpi-label"),
                    html.H3(id="fdf-kpi-3", className="kpi-value")
                ], className="kpi-card")], md=3),
                dbc.Col([html.Div([
                    html.P("Avg Revenue/FDF", className="kpi-label"),
                    html.H3(id="fdf-kpi-4", className="kpi-value")
                ], className="kpi-card")], md=3)
            ], style={"padding": "20px"})
        ]),
        
        # Charts
        html.Div([
            dbc.Row([
                dbc.Col([dcc.Graph(id="fdf-chart-1")], md=6),
                dbc.Col([dcc.Graph(id="fdf-chart-2")], md=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id="fdf-chart-3")], md=12)
            ])
        ], style={"padding": "20px"}),
        
        html.Div(className="footer")
    ])
