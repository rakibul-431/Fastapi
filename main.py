#import necessary libraries
from fastapi import FastAPI,Path,HTTPException,Query
import json

# Create FastAPI instance
app = FastAPI()

# Load patient data from JSon file
def LoadData():
    with open("patients.json",'r') as f:
        data=json.load(f)
    return data

# Define API endpoint routes
#main route
@app.get("/")
def hello():
    return {"message": "Patient Management System"}

#About patient management system route
@app.get("/about")
def about():
    return {"meassage":"A fully functionl patient management system that records patients details"}

#Get all patients route
@app.get("/patients")
def patients():
    data=LoadData()
    return data

#Get patient Details by ID route
@app.get("/patients/{patient_id}")
def patient_details(patient_id: str=Path(...,description="The Id of the patient In DB",min_lenght=1,max_lenght=500,example="P001")):
    data=LoadData()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found")

#Sort patients by field route
@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="The field to sort patients by"),
                  order:str=Query("asc",description="Sort in asc or dsc order")):
    valid_fields=['height','weight','age']
    #Check Sort_by Valid or not
    if sort_by.lower() not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid sort field. valid fields are {valid_fields}')
    #Check order Valid or not
    if order.lower() not in ['asc','dsc']:
        raise HTTPException(status_code=400,detail=f"Invalid order. valid orders are {['asc','dsc']}")
    
    #Load Data
    data=LoadData()
    #Sort Data
    sort_order = True if order.lower()=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data