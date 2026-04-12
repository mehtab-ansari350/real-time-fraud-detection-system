import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import ast

# Auto refresh
st_autorefresh(interval=5000, key="fraud_dashboard")

st.set_page_config(
    page_title="Fraud Detection System",
    layout="wide"
)

st.title("🚨 Real-Time Fraud Detection System")
st.markdown("### Enterprise Fraud Monitoring Dashboard")

# Database Connection
server = 'MEHTAB_ANSARI\\MSSQL'
database = 'FraudDetectionDB'

conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

# Load Data
query = "SELECT * FROM transactions ORDER BY id DESC"
df = pd.read_sql(query, conn)

# convert explanation string to list 
def parse_explanation(x):
    try:
        if pd.isna(x) or x == "None":
            return None
        return ast.literal_eval(x)
    except:
        return None

if "explanation" in df.columns:
    df["explanation"] = df['explanation'].apply(parse_explanation)

df["created_at"] = pd.to_datetime(df["created_at"])

# Sidebar
st.sidebar.title("Analytics Controls")

risk_filter = st.sidebar.selectbox(
    "Risk Filter",
    ["All", "High Risk", "Medium Risk", "Low Risk"]
)

# Risk Level
df["risk_level"] = pd.cut(
    df["fraud_probability"],
    bins=[0,0.3,0.7,1],
    labels=["Low Risk","Medium Risk","High Risk"]
)

if risk_filter != "All":
    df = df[df["risk_level"] == risk_filter]

# Executive Metrics
total = len(df)
fraud = df["fraud_prediction"].sum()
fraud_rate = (fraud/total)*100 if total > 0 else 0
avg_risk = df["fraud_probability"].mean()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Transactions", total)
col2.metric("Fraud Transactions", int(fraud))
col3.metric("Fraud Rate", f"{fraud_rate:.2f}%")
col4.metric("Average Risk Score", f"{avg_risk:.2f}")

st.divider()

# Alert System
# Advanced Fraud Alert Center

st.subheader(" Fraud Alert Center")

high_risk_count = len(df[df["fraud_probability"] > 0.7])
medium_risk_count = len(
    df[(df["fraud_probability"] > 0.3) & 
       (df["fraud_probability"] <= 0.7)]
)

col1, col2, col3 = st.columns(3)

col1.metric(" High Risk Alerts", high_risk_count)
col2.metric(" Medium Risk Alerts", medium_risk_count)
col3.metric(" Current Risk Level", f"{avg_risk:.2f}")

# Smart Alert Logic

if high_risk_count > 5:
    st.error(" Critical Fraud Activity Detected")

elif medium_risk_count > 10:
    st.warning(" Increasing Fraud Risk Detected")

elif avg_risk > 0.4:
    st.info(" Risk Trend Increasing")

else:
    st.success(" System Operating Normally")

st.divider()

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud Distribution")
    fig = px.pie(
        df,
        names="fraud_label"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Risk Distribution")
    fig2 = px.histogram(
        df,
        x="risk_level"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2

col3, col4 = st.columns(2)

with col3:
    st.subheader("Fraud Trend Over Time")
    fig3 = px.line(
        df,
        x="created_at",
        y="fraud_probability"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Fraud Probability Distribution")
    fig4 = px.histogram(
        df,
        x="fraud_probability"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# High Risk Table

st.subheader("High Risk Transactions")

high_risk = df[df["fraud_probability"] > 0.7]

st.dataframe(high_risk, use_container_width=True)

st.divider()

# Model Explainability

st.subheader("Model Explainability (Latest Transaction)")

try:

    explain_df = df[df["explanation"].notnull()]

    if len(explain_df) > 0:

        latest = explain_df.iloc[0]

        explanation = latest["explanation"]

        feature_names = [
            "Transaction Amount",
            "Transaction Time",
            "User Location",
            "Merchant Category",
            "Device Type",
            "Account Age",
            "Transaction Frequency",
            "Previous Fraud Count",
            "Payment Method",
            "User Risk Score"
        ]

        fig_exp = px.bar(
            x=feature_names,
            y=explanation,
            title="Feature Impact on Fraud Prediction"
        )

        st.plotly_chart(fig_exp, use_container_width=True)

    else:
        st.info("No explanation data available yet.")

except Exception as e:
    st.info("Explainability data not available")

st.divider()

#  Fraud Investigation Panel

st.subheader(" Fraud Investigation Panel")

# Top Suspicious Transactions
top_suspicious = df.sort_values(
    by="fraud_probability",
    ascending=False
).head(5)

st.markdown(" Top Suspicious Transactions")

st.dataframe(
    top_suspicious[
        ["id","fraud_probability","risk_level","created_at"]
    ],
    use_container_width=True
)

# Risk Distribution

st.markdown("Risk Level Summary")

risk_summary = df["risk_level"].value_counts().reset_index()
risk_summary.columns = ["Risk Level","Count"]

fig_risk = px.bar(
    risk_summary,
    x="Risk Level",
    y="Count",
    title="Risk Level Distribution"
)

st.plotly_chart(fig_risk, use_container_width=True)

st.divider()

# Live Fraud Monitoring 
st.subheader("Live Fraud Monitoring")

# Lastest Transactions 

st.markdown ("Latest Transactions")

latest_transactions = df.head(10)

st.dataframe(
    latest_transactions[
        ["id","fraud_probability","risk_level","created_at"]
    ],
    use_container_width=True
)

# Live Risk Trend 

st.markdown("Live Risk Trend")

live_data = df.head(20)

fig_live = px.line(
    live_data,
    x="created_at",
    y="fraud_probability",
    markers=True,
    title = "Real-Time fraud risk trend"
)

st.plotly_chart(fig_live, use_container_width=True)

# Live Risk Indicator 

live_risk = live_data["fraud_probability"].mean()

st.markdown("Live Risk Status")

if live_risk > 0.7:
    st.error("Live Fraud Spike Detected")

elif live_risk > 0.4:
    st.warning("Risk Increasing")

else:
    st.success("System Operating Normally")

st.divider()

# 
    
# Recent Transactions

st.subheader("Recent Transactions")

st.dataframe(df, use_container_width=True)

st.divider()


# Download Option

st.download_button(
    "Download Data",
    df.to_csv(index=False),
    "fraud_data.csv"
)