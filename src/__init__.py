import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database as models
from config import Settings
import paho.mqtt.client as mqtt

from src.mqtt_handler.message_handler import unwrap_message

settings = Settings()

from .sensor import router as module_router
from .user import routes as user_router
from .logs import routes as logs_router

logging.basicConfig(level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    client.subscribe(settings.MQTT_TOPIC)
    logging.info(f"Subscribed to topic {settings.MQTT_TOPIC}")

def on_message(client, userdata, msg):
    logging.info(f"Received message from topic {msg.topic}")
    try:
        unwrap_message(msg.payload.decode())
    except Exception as e:
        logging.error(f"Error while unwrapping message: {e}")

def on_publish(client, userdata, mid):
    logging.info(f"Published message with id {mid}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, settings.MQTT_CLIENT)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting mqtt_handler client...")
    client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT), 60)
    client.loop_start()
    yield
    logging.info("Stopping mqtt_handler client...")
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
