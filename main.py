from models.application import Application
from models.blog import Blog
from models.category import Category
from models.group import Group
from models.report import Report
from fastapi import FastAPI
from database import Base, engine

# Import routers correctly

from routers.application import router as application_router
from routers.groups import   router as group_router
from routers.category import router as category_router
from routers.report import router as report_router
from routers.auth import router as auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GroupsHub API", version="1.0.0")

# Include routers with correct names
app.include_router(application_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(group_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(auth_router, prefix="/api")


# Run the app using: uvicorn main:app --reload
