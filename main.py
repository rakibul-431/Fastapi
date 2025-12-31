#import necessary libraries
from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,AnyUrl,EmailStr,computed_field
from typing import Optional,List,Dict,AnyStr,Annotated
import json

# Create FastAPI instance
app = FastAPI()

#Pydantic Model for Patient data validation
class Patient(BaseModel):
    id: Annotated[str,Field(...,description="Unique identifier for the patient",example="P001")]
    name: Annotated[str,Field(...,description="full name of the patient",example="Rakibul islam")]
    age: Annotated[int,Field(...,description="Age of the patient in yeart",example=30,gt=0,lt=100)]
    email: Annotated[EmailStr,Field(default=None,description="Email address fo the patient",example="rakibul@gmail.com")]
    gender: Annotated[str,Field(...,description="Gender of the patient",examples=['Male','Female','Other'])]
    city: Annotated[str,Field(...,description="City where the patient lives",example="Dhaka")]
    disease: Annotated[str,Field(...,description="Disease diagnosed for the patient",example="Diabetes")]
    height: Annotated[float,Field(...,description="Height of the patient in foot",example=5.8,gt=3,lt=8)]
    weight : Annotated[float,Field(...,description="Weight of the patient in Kg",example=70.5,gt=10,lt=130)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "Underweight"
        elif 18.5<=self.bmi<24.9:
            return "Normal weight"
        elif 25<=self.bmi<29.9:
            return "overweight"
        else:
            return "obesity"


# Load patient data from JSon file
def LoadData():
    with open("patients.json",'r') as f:
        data=json.load(f)
    return data

#Save patient Data to Json file
def SaveData(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)

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

#Add post new patient route
@app.post("/patients")
def add_patient(patient:Patient):
    #Load Existing Data
    data=LoadData()
    #check if patient already exists
    if patient.id  in data:
        raise HTTPException(status_code=400,detail="patient with this ID already exists")
    #Add new patient
    data[patient.id]=patient.model_dump(exclude={'id'})
    #Save Data
    SaveData(data)
    return JSONResponse(status_code=201,content={"message": "Patient added successfully"})
