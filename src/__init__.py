import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .shared_state import MAIN_EVENT_LOOP

from . import database as models
from config import Settings
from src.mqtt_handler import client
from .database.helper import check_sensors_status
from .websockets.utils import push_sensor_update

settings = Settings()
from .sensor import router as module_router
from .sensor.backend_sync import sync_sensors_data
from .logs import routes as logs_router
from .sensor_data import routes as sensor_data_router
from .frequency import routes as frequency_router
from .simulation import routes as simulation_router
from .websockets import routes as websockets_router

logging.basicConfig(level=logging.INFO)

def sensors_check():
    import src.shared_state as state
    try:
        changed = check_sensors_status()
        if not changed:
            return
        if state.MAIN_EVENT_LOOP:
            state.MAIN_EVENT_LOOP.call_soon_threadsafe(
                lambda: asyncio.create_task(push_sensor_update())
            )
    except RuntimeError as re:
        logging.error(f"Runtime error while pushing websocket update: {re}")
    except Exception as e:
        logging.error(f"Error during sensors status check: {e}")

scheduler = BackgroundScheduler()
trigger = IntervalTrigger(minutes=1)
scheduler.add_job(sensors_check, trigger, misfire_grace_time=30)
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    import src.shared_state as state
    sync_sensors_data()
    state.MAIN_EVENT_LOOP = asyncio.get_event_loop()

    logging.info("Starting MQTT client...")
    client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT),60)
    client.loop_start()
    yield
    logging.info("Stopping MQTT client...")
    client.loop_stop()
    client.disconnect()

app = FastAPI(title="Sensors Admin API",
              description="Sensors Admin API is a RESTful API for managing sensors and storing their technical data.",
              version="0.1.3-dev",
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
app.include_router(logs_router.router)

app.include_router(sensor_data_router.api_router)
app.include_router(frequency_router.router)
app.include_router(simulation_router.router)
app.include_router(websockets_router.router)

# health check
@app.get("/health")
async def health():
    return {"status": "ok"}
