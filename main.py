from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

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
async def name():
    global x, y, z, date
    LastReading = f"x: {x}, y: {y}, z: {z}, date: {date}"
    return templates.TemplateResponse("home.html", context={"result":LastReading, "x":x, "y":y, "z":z, "date":date})
    

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


