from fastapi import FastAPI
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