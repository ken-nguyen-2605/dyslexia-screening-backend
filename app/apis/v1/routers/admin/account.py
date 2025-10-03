from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.enums import AccountRole, ProfileType
from app.models.profile import Profile
from app.schemas.account import AccountCreateRequest, AccountRoleSchema, AccountSchema
from app.utils.auth import hash_password, require_role

router = APIRouter(
    prefix="/admin/account",
    tags=["Admin - account"],
    responses={404: {"description": "Not found"}},
)

DEFAULT_PASSWORD = "changeme123"


@router.get("/", response_model=list[AccountSchema])
def get_all_accounts(
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_role([AccountRole.ADMIN])),
):
    return db.query(Account).all()


@router.get("/{account_id}/", response_model=AccountSchema)
def get_account_by_id(
    account_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_role([AccountRole.ADMIN])),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/", response_model=AccountSchema, status_code=201)
def create_account(
    request: AccountCreateRequest,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_role([AccountRole.ADMIN])),
):
    existing_account = db.query(Account).filter(Account.email == request.email).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    default_profile = Profile(profile_type=ProfileType.PARENT)
    new_account = Account(
        email=request.email,
        hashed_password=hash_password(DEFAULT_PASSWORD),
        role=request.role,
        profiles=[default_profile],
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


@router.patch("/{account_id}/", response_model=AccountSchema)
def change_account_role(
    account_id: int,
    request: AccountRoleSchema,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_role([AccountRole.ADMIN])),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.role = request.role
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}/", status_code=204)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_role([AccountRole.ADMIN])),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
