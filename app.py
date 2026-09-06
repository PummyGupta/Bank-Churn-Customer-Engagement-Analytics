import streamlit as st
import pandas as pd
import plotly.express as px
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

df = pd.read_csv("European_Bank (1).csv")

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
# --------------------------------------------------
# MAIN KPIs
# --------------------------------------------------

st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👥")
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.markdown("### 🚨")
    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col3:
    st.markdown("### 💚")
    st.metric(
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

fig = px.bar(
    engagement_chart,
    x="Customer Type",
    y="Churn Rate",
    title="Active vs Inactive Customer Churn",
    text="Churn Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Churn Rate (%)",
    xaxis_title="Customer Type",
    showlegend=False,
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
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

fig = px.bar(
    product_chart,
    x="Number of Products",
    y="Churn Rate",
    title="Churn Rate by Number of Products",
    text="Churn Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Churn Rate (%)",
    xaxis_title="Number of Products",
    showlegend=False,
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
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

fig = px.bar(
    product_engagement,
    x="NumOfProducts",
    y="Exited",
    color="Customer Type",
    barmode="group",
    title="Product Count + Customer Engagement vs Churn",
    text="Exited"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Number of Products",
    yaxis_title="Churn Rate (%)",
    legend_title="Customer Type",
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

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
fig = px.bar(
    high_balance_chart,
    x="Customer Type",
    y="Churn Rate",
    title="High-Balance Customers: Active vs Inactive",
    text="Churn Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Customer Type",
    yaxis_title="Churn Rate (%)",
    showlegend=False,
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
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
fig = px.pie(
    risk_status,
    names="Customer Status",
    values="Customers",
    hole=0.55,
    title="High-Value Risk Segment: Customer Status"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate="%{label}: %{value} customers<extra></extra>"
)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
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
fig = px.bar(
    geography_chart,
    x="Geography",
    y="Churn Rate",
    title="Geography-wise Customer Churn",
    text="Churn Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Geography",
    yaxis_title="Churn Rate (%)",
    showlegend=False,
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
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

    fig = px.bar(
    risk_geo_chart,
    x="Geography",
    y="Churn Rate",
    title="High-Value Risk: Churn by Geography",
    text="Churn Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Geography",
    yaxis_title="Churn Rate (%)",
    showlegend=False,
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------

# --------------------------------------------------
# HIGH-VALUE RISK BY GEOGRAPHY
# --------------------------------------------------
# --------------------------------------------------
# HIGH-VALUE RISK BY GEOGRAPHY
# --------------------------------------------------


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

    fig = px.bar(
        risk_product_chart,
        x="Number of Products",
        y="Churn Rate",
        title="High-Value Risk: Churn by Product Count",
        text="Churn Rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Number of Products",
        yaxis_title="Churn Rate (%)",
        showlegend=False,
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No high-value risk customers match the selected filters.")


# --------------------------------------------------
# RELATIONSHIP STRENGTH
# --------------------------------------------------
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

# Relationship Strength Comparison Chart

relationship_chart = pd.DataFrame({
    "Customer Group": [
        "Overall Customers",
        "Active + 2 Products"
    ],
    "Retention Rate": [
        retention_rate,
        relationship_retention
    ]
})

fig = px.bar(
    relationship_chart,
    x="Customer Group",
    y="Retention Rate",
    title="Relationship Strength: Retention Comparison",
    text="Retention Rate"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Customer Group",
    yaxis_title="Retention Rate (%)",
    showlegend=False,
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
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
# Dynamic Business Insights

st.markdown(
    f"""
- **Customer engagement:** The selected customer segment has an observed churn rate of **{churn_rate:.2f}%** and retention rate of **{retention_rate:.2f}%**.

- **Product depth:** Among the selected customers, the product-wise analysis shows how retention varies with the number of products, helping identify stronger and weaker relationship profiles.

- **High-value risk:** **{risk_count:,}** selected customers fall into the high-value risk segment, with an observed churn rate of **{risk_churn:.2f}%**.

- **Geography:** The geography-wise analysis highlights differences in observed churn across the selected regions.

- **Relationship strength:** Customers who are active and use two products show an observed retention rate of **{relationship_retention:.2f}%**.

- **Credit card ownership:** Credit card ownership should be considered alongside engagement because ownership alone provides limited differentiation in retention outcomes.
"""
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Customer Engagement & Product Utilization Analytics | "
    "Data-driven banking retention analysis | "
    "Developed by Pummy Gupta"
)