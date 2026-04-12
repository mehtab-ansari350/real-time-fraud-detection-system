import pickle
import numpy as np
import pandas as pd
import os
from database.insert_data import insert_transaction
import shap

print("Loading model...")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "ensemble_model.pkl")
scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

print("Model Path:", model_path)
print("Scaler Path:", scaler_path)

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))

#SHAP Explainer (Using one model for explation)
explainer = shap.TreeExplainer(model["xgb_balanced"])

print("Model loaded successfully!")


def predict_fraud(features):

    try:
        features = np.array(features).reshape(1, -1)
        features_df = pd.DataFrame(features)

        features_scaled = scaler.transform(features_df)

        # Ensemble Predictions
        pred1 = model["xgb_balanced"].predict_proba(features_scaled)[:,1]
        pred2 = model["xgb_high_recall"].predict_proba(features_scaled)[:,1]
        pred3 = model["lightgbm"].predict_proba(features_scaled)[:,1]

        # Average
        final_prob = (pred1 + pred2 + pred3) / 3

        prediction = (final_prob > 0.5).astype(int)

        # SHAP Explanation
        try:
            shap_values = explainer.shap_values(features_scaled)
            explanation = shap_values[0].tolist()
        except:
            explanation = []

        # Database Insertion
        insert_transaction(int(prediction[0]),float(final_prob[0]),explanation[:10])

        return {
            "fraud_prediction": int(prediction[0]),
            "fraud_probability": float(final_prob[0]),
            "explanation": explanation[:10]
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}