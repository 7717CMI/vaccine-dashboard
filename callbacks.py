from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def format_number(num):
    """Format numbers with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return f"{num:.0f}"

def filter_dataframe(df, filters):
    """Apply filters to dataframe"""
    filtered = df.copy()
    for field, values in filters.items():
        if values:
            filtered = filtered[filtered[field].isin(values)]
    return filtered

def register_all_callbacks(app, get_data_func):
    """
    Register all callbacks for the dashboard.
    Args:
        app: Dash app instance
        get_data_func: Function that returns the dataframe (lazy loading)
    """
    
    # 1. EPIDEMIOLOGY CALLBACKS
    @app.callback(
        [Output("epi-kpi-1", "children"),
         Output("epi-kpi-2", "children"),
         Output("epi-kpi-3", "children"),
         Output("epi-kpi-4", "children"),
         Output("epi-chart-1", "figure"),
         Output("epi-chart-2", "figure"),
         Output("epi-chart-3", "figure")],
        [Input("epi-year-filter", "value"),
         Input("epi-disease-filter", "value"),
         Input("epi-region-filter", "value"),
         Input("epi-income_type-filter", "value"),
         Input("epi-country-filter", "value")]
    )
    def update_epidemiology(years, diseases, regions, incomes, countries):
        try:
            df = get_data_func()  # Get data on demand
            
            # Check if data is empty
            if df.empty:
                return "No data", "No data", "No data", "No data", {}, {}, {}
            
            filters = {"year": years, "disease": diseases, "region": regions, "income_type": incomes, "country": countries}
            filtered = filter_dataframe(df, filters)
            
            # Check if filtered data is empty
            if filtered.empty:
                return "0", "0", "N/A", "0", {}, {}, {}
            
            total_prev = format_number(filtered["prevalence"].sum())
            total_inc = format_number(filtered["incidence"].sum())
            top_disease = filtered.groupby("disease")["prevalence"].sum().idxmax() if len(filtered) > 0 else "N/A"
            avg_inc_rate = format_number(filtered["incidence"].mean())
            
            # Chart 1: Prevalence by Disease
            prev_by_disease = filtered.groupby("disease")["prevalence"].sum().reset_index()
            fig1 = px.bar(prev_by_disease, x="disease", y="prevalence", title="Prevalence by Disease",
                          color="disease")
            fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
            
            # Chart 2: Incidence by Region
            inc_by_region = filtered.groupby("region")["incidence"].sum().reset_index()
            fig2 = go.Figure(data=[go.Pie(labels=inc_by_region["region"], values=inc_by_region["incidence"],
                                           hole=0.4, pull=[0.05]*len(inc_by_region))])
            fig2.update_layout(title="Incidence Distribution by Region", height=350)
            
            # Chart 3: Trend over years
            trend = filtered.groupby("year")[["prevalence", "incidence"]].sum().reset_index()
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=trend["year"], y=trend["prevalence"], name="Prevalence", mode='lines+markers'))
            fig3.add_trace(go.Scatter(x=trend["year"], y=trend["incidence"], name="Incidence", mode='lines+markers'))
            fig3.update_layout(title="Prevalence & Incidence Trend", plot_bgcolor="white", height=350)
            
            return total_prev, total_inc, top_disease, avg_inc_rate, fig1, fig2, fig3
        
        except Exception as e:
            print(f"[ERROR] Epidemiology callback failed: {e}")
            return "Error", "Error", "Error", "Error", {}, {}, {}
    
    # 2. VACCINATION RATE CALLBACKS
    @app.callback(
        [Output("vax-kpi-1", "children"),
         Output("vax-kpi-2", "children"),
         Output("vax-kpi-3", "children"),
         Output("vax-kpi-4", "children"),
         Output("vax-chart-1", "figure"),
         Output("vax-chart-2", "figure"),
         Output("vax-chart-3", "figure")],
        [Input("vax-year-filter", "value"),
         Input("vax-disease-filter", "value"),
         Input("vax-region-filter", "value"),
         Input("vax-income_type-filter", "value"),
         Input("vax-country-filter", "value")]
    )
    def update_vaccination_rate(years, diseases, regions, incomes, countries):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "disease": diseases, "region": regions, "income_type": incomes, "country": countries}
        filtered = filter_dataframe(df, filters)
        
        avg_vax_rate = f"{filtered['vaccination_rate'].mean():.1f}%"
        avg_cov_rate = f"{filtered['coverage_rate'].mean():.1f}%"
        top_region = filtered.groupby("region")["vaccination_rate"].mean().idxmax() if len(filtered) > 0 else "N/A"
        num_countries = filtered["country"].nunique()
        
        # Chart 1: Vaccination Rate by Region
        vax_by_region = filtered.groupby("region")["vaccination_rate"].mean().reset_index()
        fig1 = px.bar(vax_by_region, x="region", y="vaccination_rate", title="Avg Vaccination Rate by Region",
                      color="region")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: Distribution by Disease
        vax_by_disease = filtered.groupby("disease")["vaccination_rate"].mean().reset_index()
        fig2 = go.Figure(data=[go.Pie(labels=vax_by_disease["disease"], values=vax_by_disease["vaccination_rate"],
                                       hole=0.4)])
        fig2.update_layout(title="Vaccination Rate by Disease", height=350)
        
        # Chart 3: Trend
        trend = filtered.groupby("year")["vaccination_rate"].mean().reset_index()
        fig3 = px.line(trend, x="year", y="vaccination_rate", title="Vaccination Rate Trend", markers=True)
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return avg_vax_rate, avg_cov_rate, top_region, num_countries, fig1, fig2, fig3
    
    # 3. PRICING ANALYSIS CALLBACKS
    @app.callback(
        [Output("price-kpi-1", "children"),
         Output("price-kpi-2", "children"),
         Output("price-kpi-3", "children"),
         Output("price-kpi-4", "children"),
         Output("price-chart-1", "figure"),
         Output("price-chart-2", "figure"),
         Output("price-chart-3", "figure")],
        [Input("price-year-filter", "value"),
         Input("price-market-filter", "value"),
         Input("price-region-filter", "value"),
         Input("price-income_type-filter", "value"),
         Input("price-country-filter", "value"),
         Input("price-brand-filter", "value"),
         Input("price-price_class-filter", "value")]
    )
    def update_pricing(years, markets, regions, incomes, countries, brands, price_classes):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "market": markets, "region": regions, "income_type": incomes, 
                   "country": countries, "brand": brands, "price_class": price_classes}
        filtered = filter_dataframe(df, filters)
        
        avg_price = f"${filtered['price'].mean():.2f}"
        avg_elasticity = f"{filtered['price_elasticity'].mean():.1f}"
        top_brand = filtered.groupby("brand")["price"].mean().idxmax() if len(filtered) > 0 else "N/A"
        price_range = f"${filtered['price'].min():.0f} - ${filtered['price'].max():.0f}"
        
        # Chart 1: Price by Brand
        price_by_brand = filtered.groupby("brand")["price"].mean().reset_index().sort_values("price", ascending=False).head(10)
        fig1 = px.bar(price_by_brand, x="brand", y="price", title="Top 10 Brands by Price", color="price")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: Price Elasticity
        elasticity_data = filtered.groupby("market")["price_elasticity"].mean().reset_index()
        fig2 = px.scatter(filtered.sample(min(100, len(filtered))), x="price", y="price_elasticity", 
                          color="price_class", title="Price vs Elasticity", size="volume_units")
        fig2.update_layout(plot_bgcolor="white", height=350)
        
        # Chart 3: Price Trend
        trend = filtered.groupby("year")["price"].mean().reset_index()
        fig3 = px.line(trend, x="year", y="price", title="Average Price Trend", markers=True)
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return avg_price, avg_elasticity, top_brand, price_range, fig1, fig2, fig3
    
    # 4. CAGR ANALYSIS CALLBACKS
    @app.callback(
        [Output("cagr-kpi-1", "children"),
         Output("cagr-kpi-2", "children"),
         Output("cagr-kpi-3", "children"),
         Output("cagr-kpi-4", "children"),
         Output("cagr-chart-1", "figure"),
         Output("cagr-chart-2", "figure"),
         Output("cagr-chart-3", "figure")],
        [Input("cagr-year-filter", "value"),
         Input("cagr-market-filter", "value"),
         Input("cagr-region-filter", "value"),
         Input("cagr-income_type-filter", "value"),
         Input("cagr-country-filter", "value"),
         Input("cagr-segment-filter", "value"),
         Input("cagr-gender-filter", "value")]
    )
    def update_cagr(years, markets, regions, incomes, countries, segments, genders):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "market": markets, "region": regions, "income_type": incomes, 
                   "country": countries, "segment": segments, "gender": genders}
        filtered = filter_dataframe(df, filters)
        
        avg_cagr = f"{filtered['cagr'].mean():.2f}%"
        top_segment = filtered.groupby("segment")["cagr"].mean().idxmax() if len(filtered) > 0 else "N/A"
        max_cagr = f"{filtered['cagr'].max():.2f}%"
        min_cagr = f"{filtered['cagr'].min():.2f}%"
        
        # Chart 1: CAGR by Segment
        cagr_by_segment = filtered.groupby("segment")["cagr"].mean().reset_index()
        fig1 = px.bar(cagr_by_segment, x="segment", y="cagr", title="CAGR by Segment", color="cagr")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: CAGR by Region
        cagr_by_region = filtered.groupby("region")["cagr"].mean().reset_index()
        fig2 = go.Figure(data=[go.Pie(labels=cagr_by_region["region"], values=cagr_by_region["cagr"], hole=0.4)])
        fig2.update_layout(title="CAGR Distribution by Region", height=350)
        
        # Chart 3: CAGR vs Volume
        sample_data = filtered.sample(min(100, len(filtered)))
        fig3 = px.scatter(sample_data, x="volume_units", y="cagr", color="market", 
                          title="CAGR vs Volume", size="market_value_usd")
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return avg_cagr, top_segment, max_cagr, min_cagr, fig1, fig2, fig3
    
    # 5. MSA COMPARISON CALLBACKS
    @app.callback(
        [Output("msa-kpi-1", "children"),
         Output("msa-kpi-2", "children"),
         Output("msa-kpi-3", "children"),
         Output("msa-kpi-4", "children"),
         Output("msa-chart-1", "figure"),
         Output("msa-chart-2", "figure"),
         Output("msa-chart-3", "figure")],
        [Input("msa-year-filter", "value"),
         Input("msa-market-filter", "value"),
         Input("msa-region-filter", "value"),
         Input("msa-income_type-filter", "value"),
         Input("msa-country-filter", "value"),
         Input("msa-segment-filter", "value"),
         Input("msa-gender-filter", "value")]
    )
    def update_msa(years, markets, regions, incomes, countries, segments, genders):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "market": markets, "region": regions, "income_type": incomes, 
                   "country": countries, "segment": segments, "gender": genders}
        filtered = filter_dataframe(df, filters)
        
        total_value = format_number(filtered["value"].sum())
        total_volume = format_number(filtered["volume_units"].sum())
        avg_share = f"{filtered['share'].mean():.1f}%"
        avg_yoy = f"{filtered['yoy'].mean():.1f}%"
        
        # Chart 1: Value by Market
        value_by_market = filtered.groupby("market")["value"].sum().reset_index().sort_values("value", ascending=False).head(10)
        fig1 = px.bar(value_by_market, x="market", y="value", title="Top Markets by Value", color="value")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: Market Share
        share_data = filtered.groupby("brand")["share"].mean().reset_index().sort_values("share", ascending=False).head(8)
        fig2 = go.Figure(data=[go.Pie(labels=share_data["brand"], values=share_data["share"], hole=0.4,
                                       pull=[0.06 if i == 0 else 0.01 for i in range(len(share_data))])])
        fig2.update_layout(title="Market Share by Brand", height=350, clickmode='event+select')
        
        # Chart 3: YoY Growth Trend
        trend = filtered.groupby("year")["yoy"].mean().reset_index()
        fig3 = px.line(trend, x="year", y="yoy", title="YoY Growth Trend", markers=True)
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return total_value, total_volume, avg_share, avg_yoy, fig1, fig2, fig3
    
    # 6. PROCUREMENT ANALYSIS CALLBACKS
    @app.callback(
        [Output("proc-kpi-1", "children"),
         Output("proc-kpi-2", "children"),
         Output("proc-kpi-3", "children"),
         Output("proc-kpi-4", "children"),
         Output("proc-chart-1", "figure"),
         Output("proc-chart-2", "figure"),
         Output("proc-chart-3", "figure")],
        [Input("proc-year-filter", "value"),
         Input("proc-market-filter", "value"),
         Input("proc-region-filter", "value"),
         Input("proc-income_type-filter", "value"),
         Input("proc-country-filter", "value"),
         Input("proc-public_private-filter", "value"),
         Input("proc-brand-filter", "value")]
    )
    def update_procurement(years, markets, regions, incomes, countries, pub_priv, brands):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "market": markets, "region": regions, "income_type": incomes, 
                   "country": countries, "public_private": pub_priv, "brand": brands}
        filtered = filter_dataframe(df, filters)
        
        total_qty = format_number(filtered["qty"].sum())
        public_pct = f"{(filtered[filtered['public_private']=='Public'].shape[0]/len(filtered)*100):.1f}%" if len(filtered) > 0 else "0%"
        private_pct = f"{(filtered[filtered['public_private']=='Private'].shape[0]/len(filtered)*100):.1f}%" if len(filtered) > 0 else "0%"
        top_proc = filtered.groupby("procurement")["qty"].sum().idxmax() if len(filtered) > 0 else "N/A"
        
        # Chart 1: Qty by Procurement Type
        qty_by_proc = filtered.groupby("procurement")["qty"].sum().reset_index()
        fig1 = px.bar(qty_by_proc, x="procurement", y="qty", title="Quantity by Procurement Type", color="procurement")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: Public vs Private
        pub_priv_data = filtered.groupby("public_private")["qty"].sum().reset_index()
        fig2 = go.Figure(data=[go.Pie(labels=pub_priv_data["public_private"], values=pub_priv_data["qty"],
                                       hole=0.4, pull=[0.05, 0.05])])
        fig2.update_layout(title="Public vs Private Procurement", height=350)
        
        # Chart 3: Procurement Trend
        trend = filtered.groupby(["year", "public_private"])["qty"].sum().reset_index()
        fig3 = px.line(trend, x="year", y="qty", color="public_private", title="Procurement Trend", markers=True)
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return total_qty, public_pct, private_pct, top_proc, fig1, fig2, fig3
    
    # 7. BRAND-DEMOGRAPHIC ANALYSIS CALLBACKS
    @app.callback(
        [Output("brand-demo-kpi-1", "children"),
         Output("brand-demo-kpi-2", "children"),
         Output("brand-demo-kpi-3", "children"),
         Output("brand-demo-kpi-4", "children"),
         Output("brand-demo-chart-1", "figure"),
         Output("brand-demo-chart-2", "figure"),
         Output("brand-demo-chart-3", "figure")],
        [Input("brand-demo-year-filter", "value"),
         Input("brand-demo-market-filter", "value"),
         Input("brand-demo-region-filter", "value"),
         Input("brand-demo-income_type-filter", "value"),
         Input("brand-demo-country-filter", "value"),
         Input("brand-demo-age_group-filter", "value"),
         Input("brand-demo-gender-filter", "value"),
         Input("brand-demo-brand-filter", "value")]
    )
    def update_brand_demographic(years, markets, regions, incomes, countries, ages, genders, brands):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "market": markets, "region": regions, "income_type": incomes, 
                   "country": countries, "age_group": ages, "gender": genders, "brand": brands}
        filtered = filter_dataframe(df, filters)
        
        total_revenue = format_number(filtered["revenue"].sum())
        top_brand = filtered.groupby("brand")["revenue"].sum().idxmax() if len(filtered) > 0 else "N/A"
        top_age = filtered.groupby("age_group")["revenue"].sum().idxmax() if len(filtered) > 0 else "N/A"
        avg_revenue = format_number(filtered.groupby("brand")["revenue"].sum().mean())
        
        # Chart 1: Revenue by Age Group
        rev_by_age = filtered.groupby("age_group")["revenue"].sum().reset_index()
        fig1 = px.bar(rev_by_age, x="age_group", y="revenue", title="Revenue by Age Group", color="age_group")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: Revenue by Gender
        rev_by_gender = filtered.groupby("gender")["revenue"].sum().reset_index()
        fig2 = go.Figure(data=[go.Pie(labels=rev_by_gender["gender"], values=rev_by_gender["revenue"], hole=0.4)])
        fig2.update_layout(title="Revenue Distribution by Gender", height=350)
        
        # Chart 3: Brand Performance
        brand_perf = filtered.groupby(["brand", "age_group"])["revenue"].sum().reset_index()
        top_brands = brand_perf.groupby("brand")["revenue"].sum().nlargest(10).index
        brand_perf = brand_perf[brand_perf["brand"].isin(top_brands)]
        fig3 = px.bar(brand_perf, x="brand", y="revenue", color="age_group", 
                      title="Top 10 Brands by Age Group", barmode="stack")
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return total_revenue, top_brand, top_age, avg_revenue, fig1, fig2, fig3
    
    # 8. FDF ANALYSIS CALLBACKS
    @app.callback(
        [Output("fdf-kpi-1", "children"),
         Output("fdf-kpi-2", "children"),
         Output("fdf-kpi-3", "children"),
         Output("fdf-kpi-4", "children"),
         Output("fdf-chart-1", "figure"),
         Output("fdf-chart-2", "figure"),
         Output("fdf-chart-3", "figure")],
        [Input("fdf-year-filter", "value"),
         Input("fdf-market-filter", "value"),
         Input("fdf-region-filter", "value"),
         Input("fdf-income_type-filter", "value"),
         Input("fdf-country-filter", "value"),
         Input("fdf-brand-filter", "value"),
         Input("fdf-fdf-filter", "value"),
         Input("fdf-roa-filter", "value")]
    )
    def update_fdf(years, markets, regions, incomes, countries, brands, fdfs, roas):
        df = get_data_func()  # Get data on demand
        filters = {"year": years, "market": markets, "region": regions, "income_type": incomes, 
                   "country": countries, "brand": brands, "fdf": fdfs, "roa": roas}
        filtered = filter_dataframe(df, filters)
        
        total_revenue = format_number(filtered["revenue"].sum())
        top_fdf = filtered.groupby("fdf")["revenue"].sum().idxmax() if len(filtered) > 0 else "N/A"
        top_roa = filtered.groupby("roa")["revenue"].sum().idxmax() if len(filtered) > 0 else "N/A"
        avg_revenue = format_number(filtered.groupby("fdf")["revenue"].sum().mean())
        
        # Chart 1: Revenue by FDF
        rev_by_fdf = filtered.groupby("fdf")["revenue"].sum().reset_index()
        fig1 = px.bar(rev_by_fdf, x="fdf", y="revenue", title="Revenue by Formulation", color="fdf")
        fig1.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        
        # Chart 2: Revenue by ROA
        rev_by_roa = filtered.groupby("roa")["revenue"].sum().reset_index()
        fig2 = go.Figure(data=[go.Pie(labels=rev_by_roa["roa"], values=rev_by_roa["revenue"], 
                                       hole=0.4, pull=[0.05]*len(rev_by_roa))])
        fig2.update_layout(title="Revenue Distribution by ROA", height=350, clickmode='event+select')
        
        # Chart 3: FDF-ROA Matrix
        matrix = filtered.groupby(["fdf", "roa"])["revenue"].sum().reset_index()
        fig3 = px.bar(matrix, x="fdf", y="revenue", color="roa", 
                      title="Revenue Matrix: FDF vs ROA", barmode="group")
        fig3.update_layout(plot_bgcolor="white", height=350)
        
        return total_revenue, top_fdf, top_roa, avg_revenue, fig1, fig2, fig3
