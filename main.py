from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sql_app import schemas
from typing import List
from mongoDB.mongoConnection import DOCUMENTS, COLLECTION, add_impact_record, printDocuments, retrieveImpactData,calculateAverages
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId, Decimal128
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

LastReading = '' #Global Variable to store the last reading
x = 0 #Global Variable to store the number of readings
y = 0 #Global Variable to store the number of errors
z = 0 #Global Variable to store the number of successful readings
date  = 'N/A'

connected_clients = []
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Just to keep the connection alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

@app.get("/data/", response_class=HTMLResponse) #data list
async def name(request: Request):
    global x, y, z, date
    impacts = retrieveImpactData()
    
    return templates.TemplateResponse("home.html", {"request": request, "x": x, "y": y, "z": z, "date": date, "impacts": impacts})
    
@app.get("/", response_class=HTMLResponse) #Home
async def about(request: Request):
    impacts = retrieveImpactData()
    data = calculateAverages(impacts)
    if data is None:
        data = {
        "latestImpact": "No data available",
        "AverageForce": 0.0,
        "totalConcussions": 0,
        "totalImpacts": 0,
        "timestamps" : [],
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "impactData": data})


# Post request for upload bandwidth from local host to API
@app.post("/upload/", response_model=schemas.gyroscope)
def upload_gyroscope_data_doesnt_upload_to_db(data: schemas.gyroscope):
    global x, y, z, date
    x = data.x
    y = data.y
    z = data.z
    date = data.date
    return data


# returns the most recent Bandwidth object
@app.get("/recent/", response_model=schemas.gyroscope)
def read_last_local_value():
    val = schemas.gyroscope(x=x, y=y, z=z, date=date)
    return val

@app.post("/addImpact/", response_model=schemas.impactData)
async def add_impact_data_to_DB(data: schemas.impactData):
    # Create the document as per your schema
    date = datetime.now()
    string_date = date.strftime("%Y-%m-%d %H:%M:%S")
    print("ConcussionDetected Variable: ", data.ConcussionDetected)
    document = {
        "_id": ObjectId(),
        "date": string_date,
        "gyroscopeData1": {
            "x": data.gyroscope1.x,
            "y": data.gyroscope1.y,
            "z": data.gyroscope1.z
        },
        "gyroscopeData2": {
            "x": data.gyroscope2.x,
            "y": data.gyroscope2.y,
            "z": data.gyroscope2.z
        },
        "AccelerometerData1": {
            "x": data.accelerometer1.x,
            "y": data.accelerometer1.y,
            "z": data.accelerometer1.z
        },
        "AccelerometerData2": {
            "x": data.accelerometer2.x,
            "y": data.accelerometer2.y,
            "z": data.accelerometer2.z
        },
        "force": data.force,
        "helmetID": data.helmetID,
        "ConcussionDetected": data.ConcussionDetected
    }

    try:
        COLLECTION.insert_one(document)
        if data.ConcussionDetected:
            for ws in connected_clients:
                await ws.send_text(f"🚨 Concussion Detected for Helmet ID: {data.helmetID}")
        # Return the data in the format matching the response model
        return {
            "date": string_date,
            "gyroscope1": data.gyroscope1,
            "gyroscope2": data.gyroscope2,
            "accelerometer1": data.accelerometer1,
            "accelerometer2": data.accelerometer2,
            "force": data.force,
            "helmetID": data.helmetID,
            "ConcussionDetected": data.ConcussionDetected
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding document: {e}")

@app.get("/returnAll/", response_model=List[schemas.impactData])
def read_all_data_from_DB():
    uri = os.getenv("mongoURI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["ConcussionData"]
    collection = database["impacts"]
    documents = collection.find()

    results = retrieveImpactData()
    return results
    