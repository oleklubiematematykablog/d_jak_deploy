from fastapi import FastAPI, Response, status, Request
from fastapi import Depends, Cookie, HTTPException
import secrets
from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.secret_key = "very constant and random secret, best 64 characters"
security = HTTPBasic()
app.tokens = []

app.countpatients = -1
app.patients = []
app.howmanypatients = 0
#1

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

HTMLtemplates = Jinja2Templates(directory = "HTMLtemplates")

@app.get("/welcome")
def hello(request: Request, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	return HTMLtemplates.TemplateResponse("T4.html", {"request": request, "user": "trudnY"})

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


#@app.post("/patient", response_model = PatientResp)
#def receive_patient(pt: PatientRq):
	#app.countpatients += 1
	#app.patients.append(pt)
	#return PatientResp(id = app.countpatients, patient = pt	)

#4

#@app.get("/patient/{pk}", response_model = PatientRq)
#def searching_for_patient(pk: int):
	#if ((len(app.patients) > pk) and (pk > -1)):
		#return app.patients[pk - 1]
	#else:
		#raise HTTPException(status_code = 204, detail = "no_content")

#3.2 



@app.post("/login")
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	_username = secrets.compare_digest(credentials.username, "trudnY")
	_password = secrets.compare_digest(credentials.password, "PaC13Nt")
	if not (_username or _password):
		raise HTTPException(status_code = 401)
	else:
		session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding = "utf8")).hexdigest()
		response.set_cookie(key = "session_token", value = session_token)
		app.tokens.append(session_token)
		response.headers["Location"] = "/welcome"
		response.status_code = status.HTTP_302_FOUND
		return response
	
		

#3.3

@app.post("/logout")
def logout(*, response: Response, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	else:
		app.tokens.remove(session_token)
		return RedirectResponse("/")

		
#3.5

app.post("/patient")
def addpatient(response: Response, patient: PatientRq, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	else:
		app.patients.append(patient)
		app.howmanypatients += 1
		response.set_cookie(key = "session_token", value = session_token)
		response.headers["Location"] = f"/patient/{app.howmanypatients}"
		response.status_code = status.HTTP_302_FOUND

@app.get("/patient")
def showpatients(response: Response, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	else:
		return app.patients

@app.get("/patient/{id}")
def showpatient(response: Response, id: int, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	else:
		response.set_cookie(key = "session_token", value = session_token)
		if id in range(app.howmanypatients + 1):
			return app.patients[id]

@app.delete("/patient/{id}")
def deletepatient(response: Response, id: int, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	app.patients.pop(id, None)
	response.status_code = HTTP_204_NO_CONTENT
