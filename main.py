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
		return response

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
	return response




from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder 
import sqlite3
#import aiosqlite


class AlbumRq(BaseModel):
	title: str
	artist_id: int

class AlbumResp(BaseModel):
	AlbumId: str
	Title: str
	ArtistId: int

class Customer(BaseModel):
	customerId: int = None
	firstName: str = None
	lastName: str = None
	company: str = None
	adress: str = None
	city: str = None
	state: str = None
	country: str = None
	postalcode: str = None
	fax: str = None
	email: str = None
	supportRepId: int = None

@app.on_event("startup")
async def startup():
	app.db_connection = sqlite3.connect('chinook.db')

@app.on_event("shutdown")
async def startup():
	await app.db_connection.close()

@app.get("/tracks")
async def root(page: int = 0, per_page: int = 10):
	min = page * per_page
	max = min + per_page
	app.db_connection.row_factory = sqlite3.Row 
	if page == 0:
		tracks = app.db_connection.execute(
			f"SELECT * FROM tracks WHERE trackId >= {min} AND trackId <= {max} ").fetchall()
	else:
		tracks = app.db_connection.execute(
			f"SELECT * FROM tracks WHERE trackId > {min} AND trackId <= {max} ").fetchall()	
	return tracks

@app.get("/tracks/composers")
async def get_tracks(composer_name: str):
	app.db_connection.row_factory = lambda cursor, x: x[0]
	data = app.db_connection.execute(
		"SELECT name FROM tracks WHERE composer = ? ORDER BY name ASC", (composer_name,)).fetchall()
	if len(data) == 0:
		raise HTTPException(status_code = 404, detail = {"error": "Item not found"})
	return data

@app.post("/albums", response_model = AlbumResp)
async def add_album(response: Response, request: AlbumRq):
	artist = app.db_connection.execute(
		"SELECT * FROM artists WHERE artistId = ?", (request.artist_id,)).fetchall()
	if len(artist) == 0:
		raise HTTPException(status_code = 404, detail = {"error": "Item not found"})
	cursor = app.db_connection.execute(
		"INSERT INTO albums (title, artistId) VALUES (?,?)", (request.title, request.artist_id))
	app.db_connection.commit()
	new_album_id = cursor.lastrowid
	response.status_code = status.HTTP_201_CREATED
	return AlbumResp(AlbumId = new_album_id, Title = request.title, ArtistId = request.artist_id)

@app.get("/albums/{album_id}", response_model = AlbumResp)
async def verify_album(album_id: int):
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute(
		"SELECT * FROM albums WHERE albumId = ?", (album_id,)).fetchall()
	if len(data) == 0:
		raise HTTPException(status_code = 404, detail = {"error": "Item not found"})
	return AlbumResp(AlbumId = album_id, Title = data[0]["title"], ArtistId = data[0]["artistId"])

@app.put("/customers/{customer_id}", response_model = Customer)
async def edit_customer_data(customer_id: int, customer: Customer):
	cursor = app.db_connection.cursor()
	customer_to_update_data = cursor.execute(
		f"SELECT * FROM customers WHERE customerId = {customer_id}").fetchone()
	customer_to_update_model = Customer(**customer_to_update_data)
	update_data = customer.dict(exclude_unset = True)
	customer_updated = customer_to_update_model.copy(update = update_data)
	customer_updated = jsonable_encoder(customer_updated)
	cursor = app.db_connection.execute(
		"UPDATE customers SET * = ")

@app.get("/sales")
async def statistics(category: str):
	app.db_connection.row_factory = sqlite3.Row
	if category == "customers":
		data = app.db_connection.execute(
			'''SELECT c.customerId, c.phone, c.email, ROUND(SUM(total), 2) AS Sum
			 FROM customers c JOIN invoices i ON c.customerId = i.customerId
			 GROUP BY c.customerId ORDER BY Sum DESC, c.customerId''').fetchall()
	elif category == "genres":
		data = app.db_connection.execute('''
			SELECT g.name, SUM(quantity) AS Sum FROM genres g
			JOIN tracks t ON t.genreId = g.genreId
			JOIN invoice_items ii ON ii.trackId = t.trackId
			GROUP BY g.name ORDER BY Sum DESC, g.name''').fetchall()
	else:
		raise HTTPException(status_code = 404, detail = {"error": "Item not found"})
	return data

