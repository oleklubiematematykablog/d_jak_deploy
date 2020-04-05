from fastapi import FastAPI 
from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class PatientRq(BaseModel): #patient request
	name: str
	surename: str

class PatientResp(BaseModel): #patient response
	patientId: int
	patient: PatientRq

app = FastAPI()

#1

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

#2

@app.get("/method")
def response():
	return {"method": "GET"}

@app.post("/method")
def response():
	return {"method": "POST"}

@app.put("/method")
def response():
	return {"method": "PUT"}

@app.delete("/method")
def response():
	return {"method": "DELETE"}

#3

app.id = -1
app.patients = []


@app.post("/patient")
def receive_patient(patient: PatientRq):
	app.id += 1
	app.patients.append(patient)
	return app.patients
