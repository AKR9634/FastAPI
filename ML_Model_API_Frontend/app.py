from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, model_validator, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse
from schema.user_input import person
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION


app = FastAPI()

with open("model/Health_Insurance_Random_Forest.pkl", "rb") as f:
    model = pickle.load(f)

MODEL_VERSION = "1.0.0"

# Human Readable
@app.get("/")
def home():
    return {"message" : "Insurance Premiium Prediction API"}


# Machine Readable
@app.get("/health")
def health_check():
    return {
        "status" : "OK",
        "version" : MODEL_VERSION,
        "model_loaded" :model is not None
    }


@app.post("/predict", response_model = PredictionResponse)
def predict_premium(data:person):

    input_df = {
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }

    try:

        prediction = predict_output(input_df)
        return JSONResponse(status_code= 200, content={"response" : prediction})
    
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))