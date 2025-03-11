from models.admin import Admin
from models.application import Application
from models.blog import Blog
from models.category import Category
from models.group import Group
from models.report import Report
from fastapi import FastAPI
from database import Base, engine

# Import routers correctly
# from routers.admin import router as admin_router
from routers.application import router as application_router
# from routers.authorize import router as authorize_router
# from routers.blog import router as blog_router
from routers.groups import   router as group_router
from routers.category import router as category_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GroupsHub API", version="1.0.0")

# Include routers with correct names
# app.include_router(admin_router,prefix="/api")
app.include_router(application_router, prefix="/api")
# app.include_router(authorize_router, prefix="/api")
# app.include_router(blog_router, prefix="/api")

app.include_router(category_router, prefix="/api")
app.include_router(group_router, prefix="/api")

# app.include_router(groups_router, prefix="/api")
# app.include_router(users_router, prefix="/api")


# @app.get("/")
# def home():
#     return {"message": "Welcome to GroupsHub API"}

# Run the app using: uvicorn main:app --reload
