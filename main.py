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
	id: int
	patient: PatientRq

app.countpatients = 0
app.patients = []


@app.post("/patient", response_model = PatientResp)
def receive_patient(pt: PatientRq):
	app.countpatients += 1
	app.patients.append(pt)
	return PatientResp(id = app.countpatients, patient = pt	)

#4

@app.get("/patient/{pk}", response_model = PatientRq)
def searching_for_patient(pk: int):
	if ((app.patients.len() =< pk) and (pk > 0)):
		return app.patients[pk + 1]
	else:
		return 204

