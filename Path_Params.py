from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

def load_data():
    with open('medical.json', 'r') as file:
        data = json.load(file)

    return data

@app.get("/")
def home():
    return {'message':'Hospital Patient Data Manager!!!'}


@app.get("/about")
def about():
    return {'message':'This Website helps to manage the records of the patients of the hospital!!!'}

@app.get("/view")
def view():
    data = load_data()

    return data


@app.get("/patient/{patient_id}")
def get_patient(patient_id:str = Path(..., description="ID of the Patient", example='p1')):
    
    data = load_data()

    for patient in data:
        if patient["id"] == patient_id:
            return patient
    
    raise HTTPException(status_code=404, detail='Patient not found!!!')
    
