from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256

app = FastAPI()

#1

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def root():
	return {"Welcome": "Welcome"}

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

app.countpatients = -1
app.patients = []


@app.post("/patient", response_model = PatientResp)
def receive_patient(pt: PatientRq):
	app.countpatients += 1
	app.patients.append(pt)
	return PatientResp(id = app.countpatients, patient = pt	)

#4

@app.get("/patient/{pk}", response_model = PatientRq)
def searching_for_patient(pk: int):
	if ((len(app.patients) > pk) and (pk > -1)):
		return app.patients[pk - 1]
	else:
		raise HTTPException(status_code = 204, detail = "no_content")

#3.2 

app.secret_key = "very constant and random secret, best 64 characters"
app.users = {"trudnY": "PaC13Nt"}
app.tokens = []

@app.post("/login")
def login(user: str, password: str, response: Response):
	if user in app.users and password == app.users[user]:
		session_token = sha256(bytes(f"{user}{password}{app.secret_key}")).hexdigest()
		app.tokens.append(session_token)
		response.set_cookie(key="session_token", value = session_token)
		response = RedirectResponse(url="/welcome")
		return response
	else:
		raise HTTPException(status_code = 401)


