from fastapi import FastAPI 
from fastapi import Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class Patient(BaseModel): #patient request
	name: str
	surname: str
	patientId: int = 0

app = FastAPI()

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

app.id = -1



@app.post("/patient")
async def receive_something(patient: Patient):
	app.id += 1
	patient.patientId = app.id
	return {"id": patient.id, "patient": {"name": patient.name, "surename": patient.surname}}
