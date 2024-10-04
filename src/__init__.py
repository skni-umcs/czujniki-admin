from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import database as models
from config import Settings

settings = Settings()

# must be imported after settings creation (circular import)
from .module import router as module_router

app = FastAPI(title="Sensors Admin Panel",
              description="Sensors Admin Panel is a web application for managing sensors",
              version="0.0.1-dev",
              swagger_ui_parameters={"docExpansion": "none"},
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(module_router.api_router)
