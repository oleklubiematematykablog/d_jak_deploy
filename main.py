from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
import secrets
from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
from fastapi.templating import Jinja2Templates

app = FastAPI()

#1

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

templates = Jinja2Templates(directory = "templates")

@app.get("/welcome")
def welcome(request: Request, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	return templates.TemplateResponse("T4.html", {"request": request, "user": "trudnY"})

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
def receive_patient(pt: PatientRq, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	else:
		app.countpatients += 1
		app.patients.append(pt)
		return PatientResp(id = app.countpatients, patient = pt	)

#4

@app.get("/patient/{pk}", response_model = PatientRq)
def searching_for_patient(pk: int, session_token: str = Cookie(None)):
	if session_token not in app.tokens:
		raise HTTPException(status_code = 401)
	else:
		if ((len(app.patients) > pk) and (pk > -1)):
			return app.patients[pk - 1]
		else:
			raise HTTPException(status_code = 204, detail = "no_content")

#3.2 

app.secret_key = "very constant and random secret, best 64 characters"
security = HTTPBasic()
app.tokens = []

@app.post("/login")
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	_username = secrets.compare_digest(credentials.username, "trudnY")
	_password = secrets.compare_digest(credentials.password, "PaC13Nt")
	if _username and _password:
		session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding = "utf8")).hexdigest()
		response.set_cookie(key = "session_token", value = session_token)
		app.tokens.append(session_token)
		response.headers["Location"] = "/welcome"
		response.status_code = status.HTTP_302_FOUND
		return response
	else:
		raise HTTPException(status_code = 401)

#3.3

@app.post("/logout")
def logout(*, response: Response, session_token: str = Cookie(None)):
	if session_token in tokens:
		response.delete_cookie("session_token")
		tokens.delete(session_token)
		response.headers["Location"] = "/"
		response.status_code = status.HTTP_302_FOUND
		return RedirectResponse("/")
	else:
		raise HTTPException(status_code = 401)


