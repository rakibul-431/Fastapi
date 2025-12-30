from fastapi import FastAPI,Path
import json

app = FastAPI()

def LoadData():
    with open("patients.json",'r') as f:
        data=json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System"}

@app.get("/about")
def about():
    return {"meassage":"A fully functionl patient management system that records patients details"}

@app.get("/patients")
def patients():
    data=LoadData()
    return data
@app.get("/patients/{patient_id}")
def patient_details(patient_id: str=Path(...,description="The Id of the patient In DB",min_lenght=1,max_lenght=500,example="P001")):
    data=LoadData()
    if patient_id in data:
        return data[patient_id]
    return {"message":"patient not found"}