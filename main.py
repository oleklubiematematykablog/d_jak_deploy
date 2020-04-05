from fastapi import FastAPI 
from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

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

class PatientRq(BaseModel): #patient request
	name: str
	surename: str

class PatientResp(BaseModel): #patient response
	patientId: int
	patient: PatientRq

app.id = 0
app.patients = []


@app.post("/patient")
def receive_patient(pt: PatientRq):
	app.id += 1
	patientresp: PatientResp
	patientresp.patient = pt
	patientresp.patientId = app.id 
	app.patients.append(patientresp)
	return app.patients
