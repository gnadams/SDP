from sqlalchemy.orm import Session
from datetime import *

from . import models, schemas
def get_recent(db: Session):
    return db.query(models.Band).order_by(models.Band.id.desc()).first()


def get_num_data(db: Session):
    return db.query(models.Band).count()

def get_bw(db: Session, limit: int = 20): 
    return db.query(models.Band).order_by(models.Band.id.desc()).limit(limit).all()


def create_bw(db: Session, user: schemas.Band): #schemas.BandCreate):
    Upload = user.upload
    Download = user.download
    Ping = user.ping
    Error = False
    if (Upload == 0 and Download == 0):
        Error = True

    # Shift hour over 4 hours, does not account for daylight savings.
    time_now = datetime.now(timezone.utc) - timedelta(hours=4)
    time_now = time_now.strftime("%m/%d/%Y, %H:%M:%S") # Format into normal time.
    db_user = models.Band(date=user.date, upload=Upload, download=Download, error=Error, ping=Ping)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
