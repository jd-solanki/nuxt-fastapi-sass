from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# DB
from src.db.deps import get_db

from . import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.UserRead])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get("/{id}", response_model=schemas.UserRead)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)
