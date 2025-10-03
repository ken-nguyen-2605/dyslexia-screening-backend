from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.apis.v1.endpoints import router as api_router
from app.database import Base, engine
from app.models import Base

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include api routers
app.include_router(api_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to Slide4Church API!"}
