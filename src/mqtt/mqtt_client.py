import logging

import paho.mqtt.client as mqtt
from .message_handler import unwrap_message

from config import Settings

settings = Settings()
logging.basicConfig(level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    client.subscribe(settings.MQTT_TOPIC)
    logging.info(f"Subscribed to topic {settings.MQTT_TOPIC}")

def on_message(client, userdata, msg):
    logging.info("Received mqtt message, sending to handler")
    unwrap_message(msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, settings.MQTT_CLIENT)
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_BROKER, int(settings.MQTT_PORT), 60)

client.loop_start()