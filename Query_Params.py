from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():

    with open("medical.json", "r") as file:
        data = json.load(file)

    return data


@app.get("/")
def home():
    return {"message":"Welcome to the Hospital Data Management!!!"}

@app.get("/about")
def about():
    return {"message":"This website help to manage the data of patients visiting our hospital!!!"}

@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id:str = Path(..., description="This is the unique id of the patient!!!", examples=["p1"])):

    data = load_data()

    for patient in data:
        if(patient['id'] == patient_id):
            return patient
        
    raise HTTPException(status_code=404, detail="Details not found!!!")


@app.get("/sorted")
def sort_by(sort_by:str = Query("age", description="Field to sort the data!!!", examples = ["bmi"]), order:str = Query("asc", description="Asc or Dsc!!!")):
    data = load_data()

    if sort_by not in ["age", "weight_kg", "height_cm", "bmi"]:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be asc or dsc!!!")
    
    reverse = True if order == 'desc' else False

    sorted_patient = sorted(data, key = lambda x:x[sort_by], reverse=reverse)

    return sorted_patient
    
