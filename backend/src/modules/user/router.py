from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# DB
from src.db.deps import get_db

from . import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.UserRead])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get("/{id}", response_model=schemas.UserRead)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_or_404(db, user_id)


@router.put("/{id}", response_model=schemas.UserRead)
async def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    return crud.update_user(db, user_id, user)


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
