import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database as models
from config import Settings

from src.mqtt_handler import client
settings = Settings()


from .sensor import router as module_router
from .user import routes as user_router
from .logs import routes as logs_router

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting MQTT client...")
    client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT),60)
    client.loop_start()
    yield
    logging.info("Stopping MQTT client...")
    client.loop_stop()
    client.disconnect()

app = FastAPI(title="Sensors Admin Panel",
              description="Sensors Admin Panel is a web application for managing sensors",
              version="0.0.1-dev",
              swagger_ui_parameters={"docExpansion": "none"},
              lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(module_router.api_router)
app.include_router(user_router.router)
app.include_router(logs_router.router)

# health check
@app.get("/health")
async def health():
    return {"status": "ok"}
