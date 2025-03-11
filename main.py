from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from typing import List
from mongoDB.mongoConnection import DOCUMENTS, COLLECTION, add_impact_record, printDocuments
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId, Decimal128

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

LastReading = '' #Global Variable to store the last reading
x = 0 #Global Variable to store the number of readings
y = 0 #Global Variable to store the number of errors
z = 0 #Global Variable to store the number of successful readings
date  = 'N/A'

@app.get("/", response_class=HTMLResponse) #Home
async def name(request: Request):
    global x, y, z, date
    return templates.TemplateResponse("home.html", {"request": request, "x": x, "y": y, "z": z, "date": date})
    

# Post request for upload bandwidth from local host to API
@app.post("/upload/", response_model=schemas.gyroscope)
def upload_gyroscope_data(data: schemas.gyroscope):
    global x, y, z, date
    x = data.x
    y = data.y
    z = data.z
    date = data.date
    return data


# returns the most recent Bandwidth object
@app.get("/recent/", response_model=schemas.gyroscope)
def read_latest_value():
    val = schemas.gyroscope(x=x, y=y, z=z, date=date)
    return val

@app.get("/returnAll/", response_model=List[schemas.impactData])
def read_all_data():


    uri = "mongodb+srv://gna5:mLlcsUw7PwPefhHH@cluster08.d5vve.mongodb.net/?retryWrites=true&w=majority&appName=Cluster08"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["ConcussionData"]
    collection = database["impacts"]
    documents = collection.find()

    results = []
    for doc in documents:
        processed_doc = {
            "id": str(doc["_id"]),  # Convert ObjectId to string
            "date": doc["date"],
            "gyroscopeData": [float(item["$numberLong"]) for item in doc["gyroscopeData"]],
            "AccelerometerData": [float(item["$numberDecimal"]) for item in doc["AccelerometerData"]],
            "ConcussionDetected": doc["ConcussionDetected"]
        }
        results.append(processed_doc)
        print(processed_doc)
    return results

