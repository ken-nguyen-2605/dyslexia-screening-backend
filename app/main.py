from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.apis.v1.endpoints import router as api_router
from app.database import Base, engine
import app.models

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
    add_admin_account()


@app.get("/")
def read_root():
    return {"message": "Welcome to Slide4Church API!"}


def add_admin_account():
    """Utility function to add an admin account if none exists, for development purposes."""
    from sqlalchemy.orm import Session

    from app.database import get_db
    from app.models.account import Account
    from app.models.enums import AccountRole
    from app.utils.auth import hash_password

    db: Session = next(get_db())
    admin = db.query(Account).filter(Account.role == AccountRole.ADMIN).first()
    if not admin:
        admin_account = Account(
            email="admin@gmail.com",
            hashed_password=hash_password("admin123"),
            role=AccountRole.ADMIN,
        )
        db.add(admin_account)
        db.commit()
    db.close()
