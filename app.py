import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="YOUR_PASSWORD",
    database="atm_fraud"
)

cursor = conn.cursor()

st.title("ATM Fraud Detection Dashboard")

# Total Transactions
cursor.execute("SELECT COUNT(*) FROM TRANSACTIONS")
total_txn = cursor.fetchone()[0]

st.subheader(f"Total Transactions: {total_txn}")

# Fraud Alerts
cursor.execute("SELECT COUNT(*) FROM FRAUD_ALERT")
total_alerts = cursor.fetchone()[0]

st.subheader(f"Total Fraud Alerts: {total_alerts}")

# Fraud Table
df = pd.read_sql("SELECT * FROM FRAUD_ALERT", conn)

st.dataframe(df)

# Pie Chart
risk_df = pd.read_sql("""
SELECT RISK_LEVEL, COUNT(*) as count
FROM FRAUD_ALERT
GROUP BY RISK_LEVEL
""", conn)

fig, ax = plt.subplots()

ax.pie(
    risk_df["count"],
    labels=risk_df["RISK_LEVEL"],
    autopct='%1.1f%%'
)

st.pyplot(fig)

# Kaggle Dataset
fraud_df = pd.read_sql("""
SELECT Class, COUNT(*) as total
FROM fraud_data
GROUP BY Class
""", conn)

st.write(fraud_df)

cursor.close()
conn.close()
