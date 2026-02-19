from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, model_validator, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse


app = FastAPI()

with open("Health_Insurance_Random_Forest.pkl", "rb") as f:
    model = pickle.load(f)


tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class person(BaseModel):

    age : Annotated[int, Field(..., description= "Age of the Person!!!")]
    weight : Annotated[float, Field(..., description="Weight of the Person!!!")]
    height : Annotated[float, Field(..., description="Height of the person!!!")]
    income_lpa : Annotated[float, Field(..., description="The salary of the person in LPA!!!")]
    smoker : Annotated[bool, Field(..., description="Whether the person smokes or not!!!")]
    city : Annotated[str, Field(..., description="The city in which the person lives!!!")]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="The occupation of the person!!!")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height ** 2)

        return bmi
    

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
        
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:    
            return 3
        


@app.post("/predict")
def predict_premium(data:person):

    input_df = pd.DataFrame([{
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code= 201, content={"Predicted Category" : prediction})