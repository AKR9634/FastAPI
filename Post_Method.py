# The post method is used to sent data to the server (usually to create a new resource).

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, Optional
import json

def load_data():

    with open("medical.json", "r") as file:
        data = json.load(file)

    return data

def save_data(data):

    with open("medical.json", "w") as file:
        json.dump(data, file, indent=3)


class Patient(BaseModel):

    id : Annotated[str, Field(..., description="The Unique ID of the Patient")]
    name : Annotated[str, Field(..., description="The name of the Patient")]
    age : Annotated[int, Field(..., gt=0, le=80, description="Age must be in between 0 t0 80")]
    gender : Annotated[str, Field(..., description="The Gender of the Patient")]
    height_cm : Annotated[float, Field(..., description="Height must be in metres!!!")]
    weight_kg : Annotated[float, Field(..., description="Weight must be in Kgs!!!")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight_kg/self.height_cm**2)

        return bmi
    
    @computed_field
    @property
    def medical_verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi>18.5 and self.bmi<25:
            return "Normal"
        else:
            return "Overweight"
        

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Hospital Data Management"}

@app.get("/about")
def about():
    return {"message":"This is the API for managing Patients data in the hospital!!!"}


@app.get("/view")
def view(sort_by: Optional[str] = Query(None, description="Field to sort the data!!! ")):
    data = load_data()

    if sort_by:
        if sort_by not in ["age", "height_cm", "weight_kg", "bmi"]:
            raise HTTPException(status_code=400, detail="Not a valid key to sort!!!")
        
        data = sorted(data, key=lambda x:x[sort_by])

    return data


@app.get("/view/{patient_id}")
def view_patient(patient_id : str = Path(..., description="The Unique patient id!!!", examples=["p1"])):

    data = load_data()

    for patient in data:
        if patient["id"] == patient_id:
            return patient
    
    raise HTTPException(status_code=400, detail=f"No patient with patient id : {patient_id}")


# In FastAPI, we use @app.post() to create a POST endpoint - typically used to create data.


@app.post("/add_patient")
def add_patient(patient:Patient):

    data = load_data()

    for p in data:
        if p["id"] == patient.id:
            raise HTTPException(status_code= 400, detail = "Patient ID already exists!!!")

    data.append(patient.model_dump())

    save_data(data)

    return JSONResponse(status_code=201, content={"message" : "Patient created successfully!!!"})
