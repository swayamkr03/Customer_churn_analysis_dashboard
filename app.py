import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_csv("outputs/churn_scored_customers.csv")
    df = df.rename(
        columns={
            "ChurnProbablity": "ChurnProbability",
            "riskSegment": "RiskSegment",
        }
    )
    return df


df = load_data()

st.title("Customer Churn Analysis & Prediction Dashboard")
st.caption("Interactive dashboard built from model-generated churn probability scores.")

with st.sidebar:
    st.header("Filters")

    risk_segments = st.multiselect(
        "Risk Segment",
        sorted(df["RiskSegment"].dropna().unique()),
        default=sorted(df["RiskSegment"].dropna().unique()),
    )
    contracts = st.multiselect(
        "Contract",
        sorted(df["Contract"].dropna().unique()),
        default=sorted(df["Contract"].dropna().unique()),
    )
    internet_services = st.multiselect(
        "Internet Service",
        sorted(df["InternetService"].dropna().unique()),
        default=sorted(df["InternetService"].dropna().unique()),
    )
    payment_methods = st.multiselect(
        "Payment Method",
        sorted(df["PaymentMethod"].dropna().unique()),
        default=sorted(df["PaymentMethod"].dropna().unique()),
    )

filtered = df[
    df["RiskSegment"].isin(risk_segments)
    & df["Contract"].isin(contracts)
    & df["InternetService"].isin(internet_services)
    & df["PaymentMethod"].isin(payment_methods)
]

total_customers = len(filtered)
churned_customers = int((filtered["Churn"] == "Yes").sum())
churn_rate = churned_customers / total_customers if total_customers else 0
avg_churn_probability = filtered["ChurnProbability"].mean() if total_customers else 0
high_risk_customers = int((filtered["RiskSegment"].str.lower() == "high").sum())

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Rate", f"{churn_rate:.2%}")
col4.metric("Avg Churn Probability", f"{avg_churn_probability:.2%}")
col5.metric("High Risk Customers", f"{high_risk_customers:,}")

overview_tab, risk_tab, details_tab = st.tabs(
    ["Overview", "Risk Analysis", "Customer Details"]
)

with overview_tab:
    left, right = st.columns(2)

    with left:
        fig_contract = px.histogram(
            filtered,
            x="Contract",
            color="Churn",
            barmode="group",
            title="Churn by Contract Type",
        )
        st.plotly_chart(fig_contract, use_container_width=True)

        fig_payment = px.histogram(
            filtered,
            x="PaymentMethod",
            color="Churn",
            barmode="group",
            title="Churn by Payment Method",
        )
        st.plotly_chart(fig_payment, use_container_width=True)

    with right:
        fig_internet = px.histogram(
            filtered,
            x="InternetService",
            color="Churn",
            barmode="group",
            title="Churn by Internet Service",
        )
        st.plotly_chart(fig_internet, use_container_width=True)

        risk_counts = filtered["RiskSegment"].value_counts().reset_index()
        risk_counts.columns = ["RiskSegment", "Customers"]
        fig_risk = px.pie(
            risk_counts,
            names="RiskSegment",
            values="Customers",
            hole=0.55,
            title="Customer Risk Segments",
        )
        st.plotly_chart(fig_risk, use_container_width=True)

with risk_tab:
    left, right = st.columns(2)

    contract_risk = (
        filtered.groupby("Contract", as_index=False)["ChurnProbability"].mean()
        if total_customers
        else pd.DataFrame(columns=["Contract", "ChurnProbability"])
    )
    internet_risk = (
        filtered.groupby("InternetService", as_index=False)["ChurnProbability"].mean()
        if total_customers
        else pd.DataFrame(columns=["InternetService", "ChurnProbability"])
    )
    payment_risk = (
        filtered.groupby("PaymentMethod", as_index=False)["ChurnProbability"].mean()
        if total_customers
        else pd.DataFrame(columns=["PaymentMethod", "ChurnProbability"])
    )

    with left:
        st.plotly_chart(
            px.bar(
                contract_risk,
                x="Contract",
                y="ChurnProbability",
                title="Average Churn Probability by Contract",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.bar(
                internet_risk,
                x="InternetService",
                y="ChurnProbability",
                title="Average Churn Probability by Internet Service",
            ),
            use_container_width=True,
        )

    with right:
        st.plotly_chart(
            px.bar(
                payment_risk,
                x="PaymentMethod",
                y="ChurnProbability",
                title="Average Churn Probability by Payment Method",
            ),
            use_container_width=True,
        )
        st.plotly_chart(
            px.scatter(
                filtered,
                x="tenure",
                y="MonthlyCharges",
                size="ChurnProbability",
                color="RiskSegment",
                hover_data=["customerID", "Contract", "PaymentMethod", "Churn"],
                title="Tenure vs Monthly Charges by Risk Segment",
            ),
            use_container_width=True,
        )

with details_tab:
    st.subheader("Customer Details & High-Risk Lookup")
    customer_columns = [
        "customerID",
        "Contract",
        "InternetService",
        "PaymentMethod",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "ChurnProbability",
        "RiskSegment",
        "Churn",
    ]
    st.dataframe(
        filtered[customer_columns].sort_values("ChurnProbability", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
