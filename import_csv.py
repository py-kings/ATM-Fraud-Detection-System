--import file

import pandas as pd
import mysql.connector

df = pd.read_csv(r"C:\Users\samad\Downloads\creditcard.csv")

df = df[['Time', 'Amount', 'Class']]

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="YOUR_PASSWORD",
    database="atm_fraud"
)

cursor = conn.cursor()

for _, row in df.iterrows():

    sql = """
    INSERT INTO fraud_data (Time, Amount, Class)
    VALUES (%s, %s, %s)
    """

    values = (
        float(row['Time']),
        float(row['Amount']),
        int(row['Class'])
    )

    cursor.execute(sql, values)

conn.commit()

print("Data Imported Successfully")

cursor.close()
conn.close()
