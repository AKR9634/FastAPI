# PUT is an HTTP method used to update or replace a resource at a sepcified URL.

from fastapi import FastAPI, Path, Query, HTTPException
from typing import Annotated, Optional
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from fastapi.responses import JSONResponse
import json


def load_data():

    with open("medical.json", "r") as file:
        data = json.load(file)

    return data

def save_data(data):

    with open("medical.json", "w") as file:
        json.dump(data, file, indent=3)



class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The unique ID of the Patient!!!")]
    name:Annotated[str, Field(..., description="The name of the Patient!!!")]
    age:Annotated[int, Field(..., description="The Age of the Patient!!!")]
    gender:Annotated[str, Field(..., description="The Gender of the Patient!!!")]
    height_cm:Annotated[float, Field(..., description="The Height of the Patient!!!")]
    weight_kg:Annotated[float, Field(..., description="The Weight of the Patient!!!")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight_kg/(self.height_cm/100)**2, 2)

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
        


class Updated_Patient(BaseModel):

    id: Annotated[str, Field(description="The unique ID of the Patient!!!")]
    name:Annotated[Optional[str], Field(description="The name of the Patient!!!")]
    age:Annotated[Optional[int], Field(description="The Age of the Patient!!!")]
    gender:Annotated[Optional[str], Field(description="The Gender of the Patient!!!")]
    height_cm:Annotated[Optional[float], Field(description="The Height of the Patient!!!")]
    weight_kg:Annotated[Optional[float], Field(description="The Weight of the Patient!!!")]


app = FastAPI()

@app.get("/")
def home():
    return {"message":"This is the Hospital Management Services!!!"}

@app.get("/about")
def about():
    return {"message":"This maintains the records of all the patients of the hospital!!!"}

@app.get("/view")
def view(sort_by : Optional[str] = Query(default=None, description="The ordering key!!!")):

    data = load_data()

    if sort_by:
        if sort_by not in ["age", "height_cm", "weight_kg", "bmi"]:
            raise HTTPException(status_code=400, detail="No such key for sorting!!!")
        
        data = sorted(data, key= lambda x : x[sort_by])

    return data

@app.get("/view_patient/{patient_id}")
def view_patient(patient_id : str = Path(..., description="ID of the patient whose details are to be viewed!!!")):

    data = load_data()

    for patient in data:
        if patient["id"] == patient_id:
            return patient
        
    raise HTTPException(status_code=404, detail="No patient with this ID exists!!!")

@app.post("/add_patient")
def add_patient(patient: Patient):

    data = load_data()

    for p in data:
        if p["id"] == patient.id:
            raise HTTPException(status_code=409, detail="Already Existing Patient id!!!")
        

    p = patient.model_dump()

    data.append(p)

    save_data(data)

    return JSONResponse(status_code=201, content={"message":"Patient created succesfully!!!"})



@app.put("/update_patient")
def update_patient(patient: Updated_Patient):

    updated_patient_dict = patient.model_dump(exclude_unset=True)

    data = load_data()

    for index, p in enumerate(data):
        if p["id"] == patient.id:

            temp_pat = p
            for key, value in updated_patient_dict.items():
                temp_pat[key] = value

            temp_pat_obj = Patient(**temp_pat)

            upd_temp_pat = temp_pat_obj.model_dump()

            data[index] = upd_temp_pat

            save_data(data)

            return JSONResponse(status_code=200, content={"message":"Successfully Updated!!!"})


    raise HTTPException(status_code=404, detail="No such Patient Found!!!")


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):

    data = load_data()

    for index, p in enumerate(data):
        if p["id"] == patient_id:
            del data[index]
            save_data(data)

            return JSONResponse(status_code=200, content={"message":"Deleted Successfully!!!"})

    
    raise HTTPException(status_code=404, detail="Patient not found!!!")
