import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="*ARTist#",
    database="atm_fraud"
)

cursor = conn.cursor()

st.title("ATM Fraud Detection Dashboard")

cursor.execute("SELECT COUNT(*) FROM TRANSACTIONS")
total_txn = cursor.fetchone()[0]
st.subheader(f"Total Transactions: {total_txn}")

cursor.execute("SELECT COUNT(*) FROM FRAUD_ALERT")
total_alerts = cursor.fetchone()[0]
st.subheader(f"Total Fraud Alerts: {total_alerts}")

query = "SELECT * FROM FRAUD_ALERT"
df = pd.read_sql(query, conn)

st.write("Fraud Alerts Table")
st.dataframe(df)

risk_query = '''
SELECT RISK_LEVEL, COUNT(*) as count
FROM FRAUD_ALERT
GROUP BY RISK_LEVEL
'''

risk_df = pd.read_sql(risk_query, conn)

fig, ax = plt.subplots()

ax.pie(
    risk_df["count"],
    labels=risk_df["RISK_LEVEL"],
    autopct='%1.1f%%'
)

st.pyplot(fig)

cursor.close()
conn.close()
