from fastapi import FastAPI
from app.database import engine, Base
from app.models import Base
from fastapi.middleware.cors import CORSMiddleware


# Import routers
from app.apis.v1.endpoints import router as api_router

app = FastAPI()

origins = [
    "*",
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

@app.get("/api/health")
def health():
    return {"status": "ok"}