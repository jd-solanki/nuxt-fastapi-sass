from fastapi import FastAPI

# DB
from src.db import engine
from src.modules.user.models import Base as UserBaseModel

# Modules
from src.modules.user.router import router as user_router

# Create DB Tables
UserBaseModel.metadata.create_all(bind=engine)

app = FastAPI()

# Include user router
app.include_router(user_router, prefix="/users", tags=["users"])
