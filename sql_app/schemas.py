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