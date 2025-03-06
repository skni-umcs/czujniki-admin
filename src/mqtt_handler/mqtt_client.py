from paho.mqtt import client as mqtt
import logging
from src.mqtt_handler.message_handler import unwrap_message
from config import Settings

settings = Settings()

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
