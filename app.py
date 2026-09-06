import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Bank Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("Data/European_Bank (1).csv")

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏦 Customer Engagement & Product Utilization Analytics")
st.markdown(
    "### Bank Customer Retention & Churn Analysis Dashboard"
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Customer Filters")

geography_filter = st.sidebar.multiselect(
    "Geography",
    options=sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

product_filter = st.sidebar.multiselect(
    "Number of Products",
    options=sorted(df["NumOfProducts"].unique()),
    default=sorted(df["NumOfProducts"].unique())
)

activity_filter = st.sidebar.selectbox(
    "Customer Activity",
    options=["All", "Active", "Inactive"]
)

# Apply filters
filtered_df = df[
    (df["Geography"].isin(geography_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["NumOfProducts"].isin(product_filter))
].copy()

if activity_filter == "Active":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == 1]

elif activity_filter == "Inactive":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == 0]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_customers = len(filtered_df)

if total_customers > 0:
    churn_rate = filtered_df["Exited"].mean() * 100
    retention_rate = 100 - churn_rate
else:
    churn_rate = 0
    retention_rate = 0

# --------------------------------------------------
# MAIN KPIs
# --------------------------------------------------

st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)

st.markdown("---")

# --------------------------------------------------
# ENGAGEMENT VS CHURN
# --------------------------------------------------

st.subheader("📊 Customer Engagement vs Churn")

engagement_churn = (
    filtered_df.groupby("IsActiveMember")["Exited"]
    .mean()
    .mul(100)
)

inactive_churn = engagement_churn.get(0, 0)
active_churn = engagement_churn.get(1, 0)

col1, col2 = st.columns(2)

col1.metric(
    "Inactive Customer Churn",
    f"{inactive_churn:.2f}%"
)

col2.metric(
    "Active Customer Churn",
    f"{active_churn:.2f}%"
)

engagement_chart = pd.DataFrame({
    "Customer Type": ["Inactive", "Active"],
    "Churn Rate": [inactive_churn, active_churn]
})

st.bar_chart(
    engagement_chart.set_index("Customer Type")
)

# --------------------------------------------------
# PRODUCT-WISE CHURN
# --------------------------------------------------

st.subheader("📦 Product Utilization vs Churn")

product_churn = (
    filtered_df.groupby("NumOfProducts")["Exited"]
    .mean()
    .mul(100)
)

product_chart = product_churn.reset_index()
product_chart.columns = ["Number of Products", "Churn Rate"]

st.bar_chart(
    product_chart.set_index("Number of Products")
)

# --------------------------------------------------
# PRODUCT + ENGAGEMENT
# --------------------------------------------------

st.subheader("🔗 Product Count + Customer Engagement")

product_engagement = (
    filtered_df.groupby(
        ["NumOfProducts", "IsActiveMember"]
    )["Exited"]
    .mean()
    .mul(100)
    .reset_index()
)

product_engagement["Customer Type"] = product_engagement[
    "IsActiveMember"
].map({
    0: "Inactive",
    1: "Active"
})

product_engagement_chart = product_engagement.pivot(
    index="NumOfProducts",
    columns="Customer Type",
    values="Exited"
)

st.bar_chart(product_engagement_chart)

# --------------------------------------------------
# HIGH-BALANCE ANALYSIS
# --------------------------------------------------

st.subheader("💰 High-Balance Customers: Active vs Inactive")

balance_threshold = df["Balance"].quantile(0.75)

high_balance = filtered_df[
    filtered_df["Balance"] >= balance_threshold
]

high_balance_activity = (
    high_balance.groupby("IsActiveMember")["Exited"]
    .mean()
    .mul(100)
)

high_balance_chart = pd.DataFrame({
    "Customer Type": ["Inactive", "Active"],
    "Churn Rate": [
        high_balance_activity.get(0, 0),
        high_balance_activity.get(1, 0)
    ]
})

st.bar_chart(
    high_balance_chart.set_index("Customer Type")
)

st.caption(
    f"High-balance threshold: ₹{balance_threshold:,.2f}"
)

# --------------------------------------------------
# HIGH-VALUE RISK SEGMENT
# --------------------------------------------------

st.subheader("🚨 High-Value Risk Segment")

high_value_risk = filtered_df[
    (filtered_df["Balance"] >= balance_threshold) &
    (filtered_df["IsActiveMember"] == 0) &
    (filtered_df["Age"] >= 44)
]

risk_count = len(high_value_risk)

if risk_count > 0:
    risk_churn = high_value_risk["Exited"].mean() * 100
    risk_retention = 100 - risk_churn
else:
    risk_churn = 0
    risk_retention = 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "High-Value Risk Customers",
    f"{risk_count:,}"
)

col2.metric(
    "Risk Segment Churn",
    f"{risk_churn:.2f}%"
)

col3.metric(
    "Risk Segment Retention",
    f"{risk_retention:.2f}%"
)

risk_status = pd.DataFrame({
    "Customer Status": ["Retained", "Churned"],
    "Customers": [
        len(high_value_risk[high_value_risk["Exited"] == 0]),
        len(high_value_risk[high_value_risk["Exited"] == 1])
    ]
})

st.bar_chart(
    risk_status.set_index("Customer Status")
)

# --------------------------------------------------
# GEOGRAPHY ANALYSIS
# --------------------------------------------------

st.subheader("🌍 Geography-wise Churn")

geography_churn = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .mul(100)
)

geography_chart = geography_churn.reset_index()
geography_chart.columns = ["Geography", "Churn Rate"]

st.bar_chart(
    geography_chart.set_index("Geography")
)

# --------------------------------------------------
# HIGH-VALUE RISK BY GEOGRAPHY
# --------------------------------------------------

st.subheader("🚨 High-Value Risk: Geography-wise Churn")

if len(high_value_risk) > 0:

    risk_geo = (
        high_value_risk.groupby("Geography")["Exited"]
        .mean()
        .mul(100)
    )

    risk_geo_chart = risk_geo.reset_index()
    risk_geo_chart.columns = [
        "Geography",
        "Churn Rate"
    ]

    st.bar_chart(
        risk_geo_chart.set_index("Geography")
    )

else:
    st.info("No high-value risk customers match the selected filters.")

# --------------------------------------------------
# HIGH-VALUE RISK BY PRODUCT
# --------------------------------------------------

st.subheader("📦 High-Value Risk: Product-wise Churn")

if len(high_value_risk) > 0:

    risk_product = (
        high_value_risk.groupby("NumOfProducts")["Exited"]
        .mean()
        .mul(100)
    )

    risk_product_chart = risk_product.reset_index()
    risk_product_chart.columns = [
        "Number of Products",
        "Churn Rate"
    ]

    st.bar_chart(
        risk_product_chart.set_index("Number of Products")
    )

else:
    st.info("No high-value risk customers match the selected filters.")

# --------------------------------------------------
# RELATIONSHIP STRENGTH
# --------------------------------------------------

st.subheader("💪 Relationship Strength")

active_two_product = filtered_df[
    (filtered_df["IsActiveMember"] == 1) &
    (filtered_df["NumOfProducts"] == 2)
]

relationship_count = len(active_two_product)

if relationship_count > 0:

    relationship_retention = (
        1 - active_two_product["Exited"].mean()
    ) * 100

    relationship_index = (
        relationship_retention / retention_rate * 100
        if retention_rate > 0
        else 0
    )

else:
    relationship_retention = 0
    relationship_index = 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "Active + 2 Product Customers",
    f"{relationship_count:,}"
)

col2.metric(
    "Observed Retention",
    f"{relationship_retention:.2f}%"
)

col3.metric(
    "Relationship Strength Index",
    f"{relationship_index:.2f}"
)

# --------------------------------------------------
# CREDIT CARD STICKINESS
# --------------------------------------------------

st.subheader("💳 Credit Card Stickiness")

active_card = filtered_df[
    (filtered_df["IsActiveMember"] == 1) &
    (filtered_df["HasCrCard"] == 1)
]

if len(active_card) > 0:

    card_retention = (
        1 - active_card["Exited"].mean()
    ) * 100

    card_stickiness = (
        card_retention / retention_rate * 100
        if retention_rate > 0
        else 0
    )

else:
    card_retention = 0
    card_stickiness = 0

col1, col2 = st.columns(2)

col1.metric(
    "Active + Credit Card Retention",
    f"{card_retention:.2f}%"
)

col2.metric(
    "Credit Card Stickiness Score",
    f"{card_stickiness:.2f}"
)

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.markdown("---")

st.subheader("💡 Key Business Insights")

st.markdown("""
- **Customer engagement:** Active customers show lower observed churn than inactive customers.
- **Product depth:** Two-product customers show the strongest observed retention among the major product groups.
- **High-value risk:** High-balance, inactive, older customers form a small but highly vulnerable segment.
- **Geography:** Germany shows the highest observed churn among the three geographic groups.
- **Relationship strength:** Active customers using two products demonstrate particularly strong observed retention.
- **Credit card ownership:** Credit card ownership alone provides limited differentiation in churn outcomes.
""")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Customer Engagement & Product Utilization Analytics | "
    "Data-driven banking retention analysis"
)