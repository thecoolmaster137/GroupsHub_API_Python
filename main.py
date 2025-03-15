from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

# Import routers
from routers.application import router as application_router
from routers.groups import router as group_router
from routers.category import router as category_router
from routers.report import router as report_router
from routers.auth import router as auth_router
from routers.countries import router as countries_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GroupsHub API", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")  # Ensure correct token URL

# ✅ **Enable CORS for Frontend Access**
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Adjust this when deploying frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(application_router, prefix="/api")
app.include_router(category_router, prefix="/api", tags=["Categories"])
app.include_router(group_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(countries_router, prefix="/api")

# ✅ **Manually Define Bearer Auth for Swagger UI (Only for POST /api/categories/)**
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="GroupsHub API",
        version="1.0.0",
        description="API with JWT authentication for specific routes",
        routes=app.routes,
    )

    # Define Bearer Authentication Scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # ✅ **Apply Security Only to POST /api/categories/**
    secured_endpoints = {
        "/api/categories/": ["post"],  # Only protect POST method
        "/api/categories/{id}": ["put", "delete"],  # Protect PUT & DELETE
        "/api/applications/": ["post"],  # Protect POST
        "/api/applications/{id}": ["put", "delete"],  # Protect PUT & DELETE
        "/api/groups/{group_id}": ["put", "delete"],  # Protect PUT & DELETE
        "/api/report/": ["post"],  # Only protect POST method
        "/api/report/{id}": ["put", "delete"],  # Protect PUT & DELETE
    }

    for path, methods in secured_endpoints.items():
        if path in openapi_schema["paths"]:
            for method in methods:
                if method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # Apply custom OpenAPI settings

# ✅ **Run the app using**:
# uvicorn main:app --reload
