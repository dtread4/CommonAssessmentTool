"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.auth.router import router as auth_router
from app.clients.router import router as clients_router
from app.clients.service.ml_models_router import router as ml_models_router
from app.database import engine

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Case Management API", description="API for managing client cases", version="1.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(ml_models_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_credentials=True,
)
