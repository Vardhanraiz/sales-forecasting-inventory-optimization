import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Demand Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dashboard_data"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.10);
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 15px;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px;
    }

    .dashboard-subtitle {
        color: #9ca3af;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .insight-card {
        background-color: rgba(30, 136, 229, 0.10);
        border-left: 4px solid #1e88e5;
        padding: 18px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    required_files = {
        "sales": DATA_DIR / "cleaned_sales_data.csv",
        "monthly": DATA_DIR / "monthly_sales.csv",
        "models": DATA_DIR / "model_comparison.csv",
        "forecasts": DATA_DIR / "future_forecasts.csv",
        "anomalies": DATA_DIR / "anomaly_results.csv",
        "weekly": DATA_DIR / "weekly_sales.csv",
        "segments": DATA_DIR / "product_demand_segments.csv",
        "pca": DATA_DIR / "pca_cluster_coordinates.csv",
    }

    missing_files = [
        str(path.name)
        for path in required_files.values()
        if not path.exists()
    ]

    if missing_files:
        st.error(
            "The following required files are missing: "
            + ", ".join(missing_files)
        )
        st.stop()

    sales = pd.read_csv(required_files["sales"])
    monthly = pd.read_csv(required_files["monthly"])
    models = pd.read_csv(required_files["models"])
    forecasts = pd.read_csv(required_files["forecasts"])
    anomalies = pd.read_csv(required_files["anomalies"])
    weekly = pd.read_csv(required_files["weekly"])
    segments = pd.read_csv(required_files["segments"])
    pca = pd.read_csv(required_files["pca"])

    # Date conversions
    if "Order Date" in sales.columns:
        sales["Order Date"] = pd.to_datetime(
            sales["Order Date"],
            errors="coerce"
        )

    monthly["Date"] = pd.to_datetime(
        monthly["Date"],
        errors="coerce"
    )

    forecasts["Date"] = pd.to_datetime(
        forecasts["Date"],
        errors="coerce"
    )

    anomalies["Date"] = pd.to_datetime(
        anomalies["Date"],
        errors="coerce"
    )

    weekly["Date"] = pd.to_datetime(
        weekly["Date"],
        errors="coerce"
    )

    return (
        sales,
        monthly,
        models,
        forecasts,
        anomalies,
        weekly,
        segments,
        pca
    )


(
    sales_df,
    monthly_df,
    model_df,
    forecast_df,
    anomaly_df,
    weekly_df,
    segment_df,
    pca_df
) = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_currency(value):
    return f"${value:,.2f}"


def format_compact_currency(value):
    value = float(value)

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"

    return f"${value:,.2f}"


def style_figure(fig, height=450):

    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode="x unified",
        legend_title_text=""
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📊 Demand Intelligence")

    st.markdown(
        """
        End-to-End Sales Forecasting &  
        Demand Intelligence System
        """
    )

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Sales Overview",
            "Forecast Explorer",
            "Anomaly Report",
            "Product Demand Segments"
        ]
    )

    st.divider()

    st.caption(
        "Built as part of the XYLOFY AI Internship Project"
    )


# ============================================================
# PAGE 1 — SALES OVERVIEW
# ============================================================

if page == "Sales Overview":

    st.title("📊 Sales Overview")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'Explore historical sales performance across regions, '
        'categories, and customer activity.'
        '</p>',
        unsafe_allow_html=True
    )

    filtered_sales = sales_df.copy()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    with st.sidebar:

        st.subheader("Sales Overview Filters")

        if "Region" in sales_df.columns:

            all_regions = sorted(
                sales_df["Region"].dropna().unique()
            )

            selected_regions = st.multiselect(
                "Select Region",
                all_regions,
                default=all_regions
            )

            if selected_regions:
                filtered_sales = filtered_sales[
                    filtered_sales["Region"].isin(
                        selected_regions
                    )
                ]

        if "Category" in sales_df.columns:

            all_categories = sorted(
                sales_df["Category"].dropna().unique()
            )

            selected_categories = st.multiselect(
                "Select Category",
                all_categories,
                default=all_categories
            )

            if selected_categories:
                filtered_sales = filtered_sales[
                    filtered_sales["Category"].isin(
                        selected_categories
                    )
                ]

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_sales = filtered_sales["Sales"].sum()

    if "Order ID" in filtered_sales.columns:
        total_orders = filtered_sales["Order ID"].nunique()
    else:
        total_orders = len(filtered_sales)

    if "Customer ID" in filtered_sales.columns:
        total_customers = filtered_sales[
            "Customer ID"
        ].nunique()
    else:
        total_customers = 0

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    st.subheader("Key Performance Indicators")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Total Sales",
        format_compact_currency(total_sales)
    )

    kpi2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    kpi3.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    kpi4.metric(
        "Average Order Value",
        format_currency(average_order_value)
    )

    st.divider()

    # --------------------------------------------------------
    # SALES BY YEAR
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if "Order Date" in filtered_sales.columns:

            yearly_sales = (
                filtered_sales
                .dropna(subset=["Order Date"])
                .assign(
                    Year=lambda x: x["Order Date"].dt.year
                )
                .groupby("Year", as_index=False)["Sales"]
                .sum()
            )

            fig_year = px.bar(
                yearly_sales,
                x="Year",
                y="Sales",
                text="Sales",
                title="Total Sales by Year"
            )

            fig_year.update_traces(
                texttemplate="$%{text:.3s}",
                textposition="outside"
            )

            fig_year.update_yaxes(
                tickprefix="$",
                tickformat="~s"
            )

            st.plotly_chart(
                style_figure(fig_year),
                use_container_width=True
            )

    # --------------------------------------------------------
    # MONTHLY SALES
    # --------------------------------------------------------

    with col2:

        fig_monthly = px.line(
            monthly_df,
            x="Date",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        if "3-Month Moving Average" in monthly_df.columns:

            fig_monthly.add_trace(
                go.Scatter(
                    x=monthly_df["Date"],
                    y=monthly_df[
                        "3-Month Moving Average"
                    ],
                    mode="lines",
                    name="3-Month Moving Average"
                )
            )

        fig_monthly.update_yaxes(
            tickprefix="$",
            tickformat="~s"
        )

        st.plotly_chart(
            style_figure(fig_monthly),
            use_container_width=True
        )

    # --------------------------------------------------------
    # CATEGORY AND REGION
    # --------------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        if "Category" in filtered_sales.columns:

            category_sales = (
                filtered_sales
                .groupby("Category", as_index=False)["Sales"]
                .sum()
                .sort_values("Sales", ascending=False)
            )

            fig_category = px.bar(
                category_sales,
                x="Category",
                y="Sales",
                color="Category",
                title="Sales by Category"
            )

            fig_category.update_yaxes(
                tickprefix="$",
                tickformat="~s"
            )

            fig_category.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                style_figure(fig_category),
                use_container_width=True
            )

    with col4:

        if "Region" in filtered_sales.columns:

            region_sales = (
                filtered_sales
                .groupby("Region", as_index=False)["Sales"]
                .sum()
                .sort_values("Sales", ascending=False)
            )

            fig_region = px.pie(
                region_sales,
                names="Region",
                values="Sales",
                hole=0.45,
                title="Sales Distribution by Region"
            )

            st.plotly_chart(
                style_figure(fig_region),
                use_container_width=True
            )

    # --------------------------------------------------------
    # SALES INSIGHTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("💡 Sales Insights")

    insight1, insight2 = st.columns(2)

    if "Category" in filtered_sales.columns and not filtered_sales.empty:

        top_category = (
            filtered_sales
            .groupby("Category")["Sales"]
            .sum()
            .idxmax()
        )

        top_category_sales = (
            filtered_sales
            .groupby("Category")["Sales"]
            .sum()
            .max()
        )

        insight1.info(
            f"**Top-performing category:** {top_category}, "
            f"generating {format_currency(top_category_sales)} "
            f"in total sales."
        )

    if "Region" in filtered_sales.columns and not filtered_sales.empty:

        top_region = (
            filtered_sales
            .groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        top_region_sales = (
            filtered_sales
            .groupby("Region")["Sales"]
            .sum()
            .max()
        )

        insight2.info(
            f"**Top-performing region:** {top_region}, "
            f"with {format_currency(top_region_sales)} "
            f"in total sales."
        )


# ============================================================
# PAGE 2 — FORECAST EXPLORER
# ============================================================

elif page == "Forecast Explorer":

    st.title("📈 Forecast Explorer")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'Compare forecasting models, evaluate prediction accuracy, '
        'and explore future sales forecasts.'
        '</p>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # BEST MODEL
    # --------------------------------------------------------

    best_model_row = model_df.loc[
        model_df["MAPE"].idxmin()
    ]

    best_model = best_model_row["Model"]
    best_mape = best_model_row["MAPE"]
    best_mae = best_model_row["MAE"]
    best_rmse = best_model_row["RMSE"]

    st.subheader("🏆 Best Performing Forecast Model")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Best Model",
        best_model
    )

    col2.metric(
        "MAPE",
        f"{best_mape:.2f}%"
    )

    col3.metric(
        "MAE",
        format_compact_currency(best_mae)
    )

    col4.metric(
        "RMSE",
        format_compact_currency(best_rmse)
    )

    st.success(
        f"{best_model} achieved the lowest MAPE of "
        f"{best_mape:.2f}% and is the best-performing "
        f"model among the evaluated forecasting methods."
    )

    st.divider()

    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    st.subheader("📊 Model Performance Comparison")

    selected_metric = st.selectbox(
        "Select evaluation metric",
        ["MAPE", "MAE", "RMSE"]
    )

    metric_fig = px.bar(
        model_df,
        x="Model",
        y=selected_metric,
        color="Model",
        text=selected_metric,
        title=(
            f"{selected_metric} Comparison Across "
            f"Forecasting Models"
        )
    )

    metric_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    metric_fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        style_figure(metric_fig),
        use_container_width=True
    )

    with st.expander(
        "View Complete Model Performance Data"
    ):

        performance_table = model_df[
            ["Model", "MAE", "RMSE", "MAPE"]
        ].copy()

        st.dataframe(
            performance_table,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --------------------------------------------------------
    # FUTURE FORECASTS
    # --------------------------------------------------------

    st.subheader("🔮 3-Month Future Sales Forecast")

    forecast_fig = px.line(
        forecast_df,
        x="Date",
        y="Forecasted_Sales",
        color="Model",
        markers=True,
        title="Future Sales Forecast Comparison"
    )

    forecast_fig.update_yaxes(
        tickprefix="$",
        tickformat=","
    )

    st.plotly_chart(
        style_figure(forecast_fig),
        use_container_width=True
    )

    selected_model = st.selectbox(
        "Select a model to inspect its forecast",
        model_df["Model"].tolist()
    )

    selected_forecast = (
        forecast_df[
            forecast_df["Model"] == selected_model
        ]
        .sort_values("Date")
        .copy()
    )

    forecast_columns = st.columns(
        max(len(selected_forecast), 1)
    )

    for index, (_, row) in enumerate(
        selected_forecast.iterrows()
    ):

        with forecast_columns[index]:

            st.metric(
                row["Date"].strftime("%B %Y"),
                format_currency(
                    row["Forecasted_Sales"]
                )
            )

    st.divider()

    # --------------------------------------------------------
    # HISTORICAL + BEST MODEL
    # --------------------------------------------------------

    st.subheader(
        "📉 Historical Sales and Best-Model Forecast"
    )

    best_forecast = (
        forecast_df[
            forecast_df["Model"] == best_model
        ]
        .sort_values("Date")
        .copy()
    )

    historical_fig = go.Figure()

    historical_fig.add_trace(
        go.Scatter(
            x=monthly_df["Date"],
            y=monthly_df["Sales"],
            mode="lines+markers",
            name="Historical Sales"
        )
    )

    historical_fig.add_trace(
        go.Scatter(
            x=best_forecast["Date"],
            y=best_forecast["Forecasted_Sales"],
            mode="lines+markers",
            name=f"{best_model} Forecast"
        )
    )

    historical_fig.update_layout(
        title=(
            f"Historical Monthly Sales vs "
            f"{best_model} Future Forecast"
        ),
        xaxis_title="Date",
        yaxis_title="Sales ($)"
    )

    historical_fig.update_yaxes(
        tickprefix="$",
        tickformat=","
    )

    st.plotly_chart(
        style_figure(historical_fig, 500),
        use_container_width=True
    )

    # --------------------------------------------------------
    # FORECAST INSIGHTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("💡 Forecast Insights")

    highest_forecast_row = best_forecast.loc[
        best_forecast["Forecasted_Sales"].idxmax()
    ]

    lowest_forecast_row = best_forecast.loc[
        best_forecast["Forecasted_Sales"].idxmin()
    ]

    insight1, insight2 = st.columns(2)

    insight1.info(
        f"**Highest predicted sales:** "
        f"{format_currency(highest_forecast_row['Forecasted_Sales'])} "
        f"in {highest_forecast_row['Date'].strftime('%B %Y')}."
    )

    insight2.warning(
        f"**Lowest predicted sales:** "
        f"{format_currency(lowest_forecast_row['Forecasted_Sales'])} "
        f"in {lowest_forecast_row['Date'].strftime('%B %Y')}."
    )

    st.markdown(
        f"""
        **Business recommendation:** Based on the evaluation results,
        **{best_model}** is the preferred forecasting model because it
        achieved the lowest MAPE of **{best_mape:.2f}%**. These forecasts
        can support inventory planning, purchasing decisions, staffing,
        and promotional strategies for the next three months.
        """
    )


# ============================================================
# PAGE 3 — ANOMALY REPORT
# ============================================================

elif page == "Anomaly Report":

    st.title("🚨 Anomaly Report")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'Detect unusual weekly sales behaviour using Isolation Forest '
        'and Rolling Z-Score methods.'
        '</p>',
        unsafe_allow_html=True
    )

    total_anomalies = len(anomaly_df)

    isolation_count = anomaly_df[
        "Isolation Forest"
    ].fillna(False).astype(bool).sum()

    zscore_count = anomaly_df[
        "Z-Score"
    ].fillna(False).astype(bool).sum()

    both_count = (
        anomaly_df["Detection Result"]
        .eq("Detected by Both")
        .sum()
    )

    st.subheader("Anomaly Detection Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Unique Anomalous Weeks",
        f"{total_anomalies}"
    )

    col2.metric(
        "Isolation Forest",
        f"{isolation_count}"
    )

    col3.metric(
        "Z-Score",
        f"{zscore_count}"
    )

    col4.metric(
        "Detected by Both",
        f"{both_count}"
    )

    st.info(
        f"{total_anomalies} unique anomalous weeks were "
        f"detected across both anomaly detection methods."
    )

    st.divider()

    # --------------------------------------------------------
    # WEEKLY SALES WITH ANOMALIES
    # --------------------------------------------------------

    st.subheader("📈 Weekly Sales with Detected Anomalies")

    anomaly_fig = go.Figure()

    anomaly_fig.add_trace(
        go.Scatter(
            x=weekly_df["Date"],
            y=weekly_df["Sales"],
            mode="lines",
            name="Weekly Sales"
        )
    )

    detection_types = anomaly_df[
        "Detection Result"
    ].dropna().unique()

    for detection_type in detection_types:

        subset = anomaly_df[
            anomaly_df["Detection Result"]
            == detection_type
        ]

        anomaly_fig.add_trace(
            go.Scatter(
                x=subset["Date"],
                y=subset["Sales"],
                mode="markers",
                marker=dict(size=11),
                name=detection_type
            )
        )

    anomaly_fig.update_layout(
        title="Weekly Sales and Anomaly Detection Results",
        xaxis_title="Date",
        yaxis_title="Weekly Sales ($)"
    )

    anomaly_fig.update_yaxes(
        tickprefix="$",
        tickformat=","
    )

    st.plotly_chart(
        style_figure(anomaly_fig, 550),
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # METHOD COMPARISON
    # --------------------------------------------------------

    st.subheader("🔍 Detection Method Comparison")

    detection_summary = (
        anomaly_df[
            "Detection Result"
        ]
        .value_counts()
        .reset_index()
    )

    detection_summary.columns = [
        "Detection Result",
        "Count"
    ]

    col1, col2 = st.columns(2)

    with col1:

        comparison_fig = px.bar(
            detection_summary,
            x="Detection Result",
            y="Count",
            color="Detection Result",
            text="Count",
            title="Anomalies by Detection Method"
        )

        comparison_fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            style_figure(comparison_fig),
            use_container_width=True
        )

    with col2:

        pie_fig = px.pie(
            detection_summary,
            names="Detection Result",
            values="Count",
            hole=0.45,
            title="Detection Result Distribution"
        )

        st.plotly_chart(
            style_figure(pie_fig),
            use_container_width=True
        )

    # --------------------------------------------------------
    # FILTERED ANOMALY TABLE
    # --------------------------------------------------------

    st.divider()
    st.subheader("📋 Anomaly Details")

    detection_options = [
        "All"
    ] + sorted(
        anomaly_df[
            "Detection Result"
        ].dropna().unique().tolist()
    )

    selected_detection = st.selectbox(
        "Filter anomalies by detection result",
        detection_options
    )

    if selected_detection == "All":
        filtered_anomalies = anomaly_df.copy()
    else:
        filtered_anomalies = anomaly_df[
            anomaly_df["Detection Result"]
            == selected_detection
        ].copy()

    display_anomalies = filtered_anomalies.copy()

    display_anomalies["Date"] = (
        display_anomalies["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    display_anomalies["Sales"] = (
        display_anomalies["Sales"]
        .round(2)
    )

    st.dataframe(
        display_anomalies,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # ANOMALY INSIGHTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("💡 Anomaly Insights")

    highest_anomaly = anomaly_df.loc[
        anomaly_df["Sales"].idxmax()
    ]

    lowest_anomaly = anomaly_df.loc[
        anomaly_df["Sales"].idxmin()
    ]

    insight1, insight2 = st.columns(2)

    insight1.warning(
        f"**Largest anomalous sales spike:** "
        f"{format_currency(highest_anomaly['Sales'])} "
        f"on {highest_anomaly['Date'].strftime('%d %B %Y')}."
    )

    insight2.info(
        f"**Lowest anomalous sales value:** "
        f"{format_currency(lowest_anomaly['Sales'])} "
        f"on {lowest_anomaly['Date'].strftime('%d %B %Y')}."
    )

    st.markdown(
        """
        **Business recommendation:** Anomalies should not automatically
        be treated as errors. Large sales spikes may result from seasonal
        demand, promotions, holiday shopping, or unusually large orders.
        Sharp drops may indicate stock shortages, weak demand, operational
        disruptions, or incomplete sales activity. Events detected by both
        methods deserve the highest investigation priority.
        """
    )


# ============================================================
# PAGE 4 — PRODUCT DEMAND SEGMENTS
# ============================================================

elif page == "Product Demand Segments":

    st.title("📦 Product Demand Segments")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'Explore K-Means product segmentation, PCA visualization, '
        'demand characteristics, and inventory strategies.'
        '</p>',
        unsafe_allow_html=True
    )

    total_products = len(segment_df)

    total_clusters = segment_df[
        "Demand_Cluster"
    ].nunique()

    st.info(
        f"{total_products} product sub-categories were grouped "
        f"into {total_clusters} demand clusters."
    )

    # --------------------------------------------------------
    # CLUSTER SUMMARY KPIs
    # --------------------------------------------------------

    st.subheader("Demand Cluster Summary")

    cluster_counts = (
        segment_df[
            "Demand_Cluster"
        ]
        .value_counts()
        .reset_index()
    )

    cluster_counts.columns = [
        "Demand Cluster",
        "Products"
    ]

    metric_columns = st.columns(
        len(cluster_counts)
    )

    for index, row in cluster_counts.iterrows():

        with metric_columns[index]:

            st.metric(
                row["Demand Cluster"],
                int(row["Products"])
            )

    st.divider()

    # --------------------------------------------------------
    # PCA CLUSTER VISUALIZATION
    # --------------------------------------------------------

    st.subheader("🧩 PCA Demand Cluster Visualization")

    pca_fig = px.scatter(
        pca_df,
        x="PCA_Component_1",
        y="PCA_Component_2",
        color="Demand_Cluster",
        text="Sub-Category",
        hover_name="Sub-Category",
        hover_data={
            "Total_Sales": ":,.2f",
            "Sales_Growth_Rate": ":.2f",
            "Sales_Volatility": ":,.2f",
            "Average_Order_Value": ":,.2f",
            "PCA_Component_1": ":.3f",
            "PCA_Component_2": ":.3f"
        },
        title=(
            "Product Demand Segmentation Using "
            "K-Means and PCA"
        )
    )

    pca_fig.update_traces(
        marker=dict(size=14),
        textposition="top center"
    )

    pca_fig.update_layout(
        legend_title="Demand Cluster"
    )

    st.plotly_chart(
        style_figure(pca_fig, 650),
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # CLUSTER FILTER
    # --------------------------------------------------------

    st.subheader("🔎 Explore Products by Demand Cluster")

    cluster_options = [
        "All Clusters"
    ] + sorted(
        segment_df[
            "Demand_Cluster"
        ].dropna().unique().tolist()
    )

    selected_cluster = st.selectbox(
        "Select demand cluster",
        cluster_options
    )

    if selected_cluster == "All Clusters":
        filtered_segments = segment_df.copy()
    else:
        filtered_segments = segment_df[
            segment_df["Demand_Cluster"]
            == selected_cluster
        ].copy()

    # --------------------------------------------------------
    # SEGMENT CHART
    # --------------------------------------------------------

    segment_chart = px.scatter(
        filtered_segments,
        x="Total_Sales",
        y="Sales_Growth_Rate",
        size="Average_Order_Value",
        color="Demand_Cluster",
        hover_name="Sub-Category",
        hover_data={
            "Sales_Volatility": ":,.2f",
            "Average_Order_Value": ":,.2f"
        },
        title="Total Sales vs Sales Growth Rate"
    )

    segment_chart.update_xaxes(
        tickprefix="$",
        tickformat="~s"
    )

    segment_chart.update_yaxes(
        ticksuffix="%"
    )

    st.plotly_chart(
        style_figure(segment_chart, 550),
        use_container_width=True
    )

    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

    st.subheader("📋 Product Demand Details")

    display_columns = [
        "Sub-Category",
        "Total_Sales",
        "Sales_Growth_Rate",
        "Sales_Volatility",
        "Average_Order_Value",
        "Demand_Cluster",
        "Stocking_Strategy"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in filtered_segments.columns
    ]

    display_segments = filtered_segments[
        available_columns
    ].copy()

    numeric_columns = [
        "Total_Sales",
        "Sales_Growth_Rate",
        "Sales_Volatility",
        "Average_Order_Value"
    ]

    for column in numeric_columns:
        if column in display_segments.columns:
            display_segments[column] = (
                display_segments[column].round(2)
            )

    st.dataframe(
        display_segments,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # CLUSTER STRATEGIES
    # --------------------------------------------------------

    st.divider()
    st.subheader("💡 Inventory Strategy by Demand Cluster")

    strategies = {
        "Premium High-Value, Volatile Demand": (
            "Maintain controlled safety stock and use frequent "
            "forecast updates. Avoid excessive inventory because "
            "these products have high value and volatile demand."
        ),

        "Low-Volume, Stable Demand": (
            "Maintain lean inventory with regular replenishment. "
            "Because demand is relatively stable and sales volume "
            "is lower, excessive safety stock is unnecessary."
        ),

        "High-Volume, Core Demand": (
            "Maintain higher safety stock and prioritize product "
            "availability. Stockouts in these core products can "
            "have a significant effect on overall revenue."
        ),

        "Irregular High-Growth Demand": (
            "Use flexible replenishment and closely monitor demand "
            "changes. Avoid relying only on historical averages "
            "because rapid growth may make past patterns misleading."
        )
    }

    for cluster_name in segment_df[
        "Demand_Cluster"
    ].dropna().unique():

        product_names = (
            segment_df.loc[
                segment_df["Demand_Cluster"]
                == cluster_name,
                "Sub-Category"
            ]
            .tolist()
        )

        with st.expander(
            f"{cluster_name} — {len(product_names)} products"
        ):

            st.write(
                "**Products:** "
                + ", ".join(product_names)
            )

            st.write(
                "**Recommended strategy:** "
                + strategies.get(
                    cluster_name,
                    "Monitor demand regularly and adjust "
                    "inventory levels accordingly."
                )
            )

    # --------------------------------------------------------
    # KEY PRODUCT INSIGHTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("📌 Key Product Insights")

    highest_sales_product = segment_df.loc[
        segment_df["Total_Sales"].idxmax()
    ]

    highest_growth_product = segment_df.loc[
        segment_df["Sales_Growth_Rate"].idxmax()
    ]

    insight1, insight2 = st.columns(2)

    insight1.info(
        f"**Highest total sales:** "
        f"{highest_sales_product['Sub-Category']} with "
        f"{format_currency(highest_sales_product['Total_Sales'])}."
    )

    insight2.warning(
        f"**Highest sales growth:** "
        f"{highest_growth_product['Sub-Category']} at "
        f"{highest_growth_product['Sales_Growth_Rate']:.2f}%."
    )
