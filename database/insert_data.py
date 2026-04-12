from database.db_connection import conn

def insert_transaction(prediction, probability,explanation=None):

    cursor = conn.cursor()

    label = "Fraud" if prediction == 1 else "Legitimate"

    cursor.execute("""
        INSERT INTO transactions 
        (fraud_prediction, fraud_probability,fraud_label,explanation)
        VALUES (?, ?, ?, ?)
    """, prediction, probability,label,str(explanation))

    conn.commit()

    print("Transaction inserted successfully")