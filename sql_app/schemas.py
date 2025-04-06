from pydantic import BaseModel


# Schema for how the API Requests need to be
class BandBase(BaseModel):
    date: str
    upload: float
    download : float
    ping: float


class Band(BandBase):
    id: int
    error: bool

    class Config:
        orm_mode = True

class gyroscope(BaseModel):
    date: str
    x: float
    y: float
    z: float



class gyroscopeData(BaseModel):
    x: float
    y: float
    z: float

class accelerometerData(BaseModel):
    x: float
    y: float
    z: float

class impactData(BaseModel):
    date: str
    gyroscope1: gyroscopeData
    gyroscope2: gyroscopeData
    accelerometer1: accelerometerData
    accelerometer2: accelerometerData
    force: float
    helmetID: int
    ConcussionDetected: bool

    