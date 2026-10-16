import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="PayGuard AI", page_icon="🛡️", layout="wide")
st.title("🛡️ PayGuard AI")
st.write("A simple payment risk analysis prototype.")
st.warning("Demo only: uses fictional data and simple rules. Not connected to PayPal or any bank.")

df = pd.read_csv("sample_transactions.csv")

def assess_risk(row):
    score = 0
    reasons = []
    if row["amount"] >= 1000:
        score += 40
        reasons.append("High transaction amount")
    if row["country_mismatch"] == "Yes":
        score += 35
        reasons.append("Country mismatch")
    if row["failed_attempts"] >= 3:
        score += 25
        reasons.append("Multiple failed attempts")
    score = min(score, 100)
    level = "High" if score >= 60 else "Medium" if score >= 30 else "Low"
    explanation = ", ".join(reasons) if reasons else "No demo rules triggered"
    return pd.Series([score, level, explanation])

df[["risk_score", "risk_level", "explanation"]] = df.apply(assess_risk, axis=1)
st.metric("Total transactions", len(df))
st.subheader("Transactions by risk level")
counts = df["risk_level"].value_counts().reset_index()
counts.columns = ["Risk Level", "Count"]
st.plotly_chart(px.bar(counts, x="Risk Level", y="Count"), use_container_width=True)
st.subheader("Transaction details")
st.dataframe(df, use_container_width=True, hide_index=True)
st.subheader("Check a sample transaction")
with st.form("check_transaction"):
    amount = st.number_input("Amount", min_value=0.0, value=250.0)
    mismatch = st.selectbox("Country mismatch?", ["No", "Yes"])
    attempts = st.number_input("Failed attempts", min_value=0, value=0, step=1)
    check = st.form_submit_button("Check risk")
if check:
    sample = pd.Series({"amount": amount, "country_mismatch": mismatch, "failed_attempts": attempts})
    score, level, explanation = assess_risk(sample)
    st.metric("Demo risk score", f"{int(score)}/100")
    st.write("Risk level:", level)
    st.write("Reason:", explanation)
st.caption("Educational prototype only. Do not use for real payment decisions.")
