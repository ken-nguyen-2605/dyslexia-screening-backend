from fastapi import FastAPI
from app.database import engine, Base
from app.models import Base
app = FastAPI()
 
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Slide4Church API!"}
