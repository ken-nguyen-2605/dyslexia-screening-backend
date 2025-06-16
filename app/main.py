from fastapi import FastAPI
from app.database import engine, Base
from app.models import Base

# Import routers
from app.apis.v1.endpoints import router as api_router

app = FastAPI()

# Include api routers
app.include_router(api_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Slide4Church API!"}
