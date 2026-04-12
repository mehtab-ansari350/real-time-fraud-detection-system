from fastapi import FastAPI
from api.schema import Transaction
from src.predict import predict_fraud
from database.insert_data import insert_transaction
import numpy as np

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Real-Time Fraud Detection API Running"}


@app.post("/predict")
def predict(transaction: Transaction):

    try:
        result = predict_fraud(transaction.features)

        #insert into database 
        insert_transaction(
            result["fraud_prediction"],
            result["fraud_probability"]
            )
        
        return result
    
    except Exception as e:
        return{"error": str(e)}


@app.get("/test")
def test():
    dummy = np.random.rand(359).tolist()
    result = predict_fraud(dummy)

    #Insert test data also
    insert_transaction(
        result["fraud_prediction"],
        result["fraud_probability"]
    )

    return result