
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Sales Forecasting & Demand Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        padding: 18px;
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# DATA PATH
# ------------------------------------------------------------

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "dashboard_data"


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

@st.cache_data
def load_data():

    cleaned_sales = pd.read_csv(
        DATA_DIR / "cleaned_sales_data.csv",
        parse_dates=["Order Date", "Ship Date"]
    )

    monthly_sales = pd.read_csv(
        DATA_DIR / "monthly_sales.csv",
        parse_dates=["Date"]
    )

    model_comparison = pd.read_csv(
        DATA_DIR / "model_comparison.csv"
    )

    future_forecasts = pd.read_csv(
        DATA_DIR / "future_forecasts.csv",
        parse_dates=["Date"]
    )

    anomaly_results = pd.read_csv(
        DATA_DIR / "anomaly_results.csv",
        parse_dates=["Date"]
    )

    weekly_sales = pd.read_csv(
        DATA_DIR / "weekly_sales.csv",
        parse_dates=["Date"]
    )

    product_segments = pd.read_csv(
        DATA_DIR / "product_demand_segments.csv"
    )

    pca_coordinates = pd.read_csv(
        DATA_DIR / "pca_cluster_coordinates.csv"
    )

    return (
        cleaned_sales,
        monthly_sales,
        model_comparison,
        future_forecasts,
        anomaly_results,
        weekly_sales,
        product_segments,
        pca_coordinates
    )


try:

    (
        df,
        monthly_sales,
        model_comparison,
        future_forecasts,
        anomaly_results,
        weekly_sales,
        product_segments,
        pca_coordinates
    ) = load_data()

except Exception as error:

    st.error(
        "The dashboard could not load the required data files."
    )

    st.exception(error)
    st.stop()


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title("📊 Demand Intelligence")

st.sidebar.markdown(
    "End-to-End Sales Forecasting & Demand Intelligence System"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Product Demand Segments"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Built as part of the XYLOFY AI Internship Project"
)


# ------------------------------------------------------------
# PAGE 1 — SALES OVERVIEW
# ------------------------------------------------------------

if page == "Sales Overview":

    st.markdown(
        '<div class="main-title">Sales Overview Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor historical revenue, orders, customers, '
        'categories and regional sales performance.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # INTERACTIVE FILTERS
    # --------------------------------------------------------

    st.sidebar.subheader("Sales Overview Filters")

    available_regions = sorted(
        df["Region"].dropna().unique().tolist()
    )

    available_categories = sorted(
        df["Category"].dropna().unique().tolist()
    )


    selected_regions = st.sidebar.multiselect(
        "Select Region",
        options=available_regions,
        default=available_regions
    )


    selected_categories = st.sidebar.multiselect(
        "Select Category",
        options=available_categories,
        default=available_categories
    )


    # Apply selected filters
    filtered_df = df[
        (df["Region"].isin(selected_regions))
        &
        (df["Category"].isin(selected_categories))
    ].copy()


    # Stop gracefully if no data matches the filters
    if filtered_df.empty:

        st.warning(
            "No sales records match the selected filters. "
            "Please select at least one region and one category."
        )

        st.stop()


    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_sales = filtered_df["Sales"].sum()

    total_orders = filtered_df["Order ID"].nunique()

    total_customers = filtered_df["Customer ID"].nunique()

    average_order_value = (
        filtered_df
        .groupby("Order ID")["Sales"]
        .sum()
        .mean()
    )


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader("Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.2f}"
        )


    with col2:

        st.metric(
            label="Total Orders",
            value=f"{total_orders:,}"
        )


    with col3:

        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}"
        )


    with col4:

        st.metric(
            label="Average Order Value",
            value=f"${average_order_value:,.2f}"
        )


    st.divider()


    # --------------------------------------------------------
    # TOTAL SALES BY YEAR
    # --------------------------------------------------------

    yearly_sales = (
        filtered_df
        .groupby("Year", as_index=False)["Sales"]
        .sum()
        .sort_values("Year")
    )


    fig_yearly = px.bar(
        yearly_sales,
        x="Year",
        y="Sales",
        title="Total Sales by Year",
        text_auto=".3s"
    )


    fig_yearly.update_layout(
        xaxis_title="Year",
        yaxis_title="Sales ($)",
        hovermode="x unified"
    )


    fig_yearly.update_traces(
        hovertemplate=(
            "<b>Year:</b> %{x}<br>"
            "<b>Sales:</b> $%{y:,.2f}"
            "<extra></extra>"
        )
    )


    # --------------------------------------------------------
    # MONTHLY SALES TREND
    # --------------------------------------------------------

    monthly_trend = (
        filtered_df
        .set_index("Order Date")
        .resample("MS")["Sales"]
        .sum()
        .reset_index()
    )


    fig_monthly = px.line(
        monthly_trend,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True
    )


    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales ($)",
        hovermode="x unified"
    )


    fig_monthly.update_traces(
        hovertemplate=(
            "<b>Month:</b> %{x|%B %Y}<br>"
            "<b>Sales:</b> $%{y:,.2f}"
            "<extra></extra>"
        )
    )


    # Display first row of charts
    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        st.plotly_chart(
            fig_yearly,
            use_container_width=True
        )


    with chart_col2:

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )


    # --------------------------------------------------------
    # SALES BY CATEGORY
    # --------------------------------------------------------

    category_sales = (
        filtered_df
        .groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=True)
    )


    fig_category = px.bar(
        category_sales,
        x="Sales",
        y="Category",
        orientation="h",
        title="Sales by Category",
        text_auto=".3s"
    )


    fig_category.update_layout(
        xaxis_title="Sales ($)",
        yaxis_title="Category"
    )


    fig_category.update_traces(
        hovertemplate=(
            "<b>Category:</b> %{y}<br>"
            "<b>Sales:</b> $%{x:,.2f}"
            "<extra></extra>"
        )
    )


    # --------------------------------------------------------
    # SALES BY REGION
    # --------------------------------------------------------

    region_sales = (
        filtered_df
        .groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=True)
    )


    fig_region = px.bar(
        region_sales,
        x="Sales",
        y="Region",
        orientation="h",
        title="Sales by Region",
        text_auto=".3s"
    )


    fig_region.update_layout(
        xaxis_title="Sales ($)",
        yaxis_title="Region"
    )


    fig_region.update_traces(
        hovertemplate=(
            "<b>Region:</b> %{y}<br>"
            "<b>Sales:</b> $%{x:,.2f}"
            "<extra></extra>"
        )
    )


    # Display second row of charts
    chart_col3, chart_col4 = st.columns(2)


    with chart_col3:

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


    with chart_col4:

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )


    # --------------------------------------------------------
    # AUTOMATIC BUSINESS INSIGHTS
    # --------------------------------------------------------

    st.divider()

    st.subheader("Business Insights")


    # Find best year
    best_year_row = yearly_sales.loc[
        yearly_sales["Sales"].idxmax()
    ]

    best_year = int(best_year_row["Year"])

    best_year_sales = best_year_row["Sales"]


    # Find strongest category
    top_category_row = category_sales.loc[
        category_sales["Sales"].idxmax()
    ]

    top_category = top_category_row["Category"]

    top_category_sales = top_category_row["Sales"]


    # Find strongest region
    top_region_row = region_sales.loc[
        region_sales["Sales"].idxmax()
    ]

    top_region = top_region_row["Region"]

    top_region_sales = top_region_row["Sales"]


    insight_col1, insight_col2, insight_col3 = st.columns(3)


    with insight_col1:

        st.info(
            f"Best-performing year: {best_year}, "
            f"with sales of ${best_year_sales:,.2f}."
        )


    with insight_col2:

        st.info(
            f"Top category: {top_category}, "
            f"generating ${top_category_sales:,.2f}."
        )


    with insight_col3:

        st.info(
            f"Top region: {top_region}, "
            f"generating ${top_region_sales:,.2f}."
        )


    # --------------------------------------------------------
    # FILTER SUMMARY
    # --------------------------------------------------------

    st.caption(
        f"Showing {len(filtered_df):,} sales records | "
        f"{len(selected_regions)} region(s) selected | "
        f"{len(selected_categories)} category/categories selected"
    )


# ------------------------------------------------------------
# PAGE 2 — FORECAST EXPLORER
# ------------------------------------------------------------

elif page == "Forecast Explorer":

    st.title("Forecast Explorer")

    st.info(
        "This page will display model performance, "
        "future forecasts, category forecasts and region forecasts."
    )


# ------------------------------------------------------------
# PAGE 3 — ANOMALY REPORT
# ------------------------------------------------------------

elif page == "Anomaly Report":

    st.title("Anomaly Report")

    st.info(
        f"{len(anomaly_results)} unique anomalous weeks "
        "were detected across both anomaly detection methods."
    )


# ------------------------------------------------------------
# PAGE 4 — PRODUCT DEMAND SEGMENTS
# ------------------------------------------------------------

elif page == "Product Demand Segments":

    st.title("Product Demand Segments")

    st.info(
        f"{len(product_segments)} product sub-categories "
        f"were grouped into "
        f"{product_segments['Cluster'].nunique()} demand clusters."
    )
