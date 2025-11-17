from paho.mqtt import client as mqtt
from config import Settings
import logging
import json
from src.database.core import get_db_session
from src.sensor_data.connector import add_sensor_data

settings = Settings()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, settings.MQTT_CLIENT)

def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(settings.MQTT_TOPIC_SEND)
    client.subscribe(settings.MQTT_TOPIC_RECEIVE)
    logging.info(f"MQTT ready for send and receive")

def on_message(client, userdata, msg):
    if msg.topic != settings.MQTT_TOPIC_RECEIVE:
        return
    try:
        unwrap_message(msg.payload.decode())
    except Exception as e:
        logging.error(f"Error while unwrapping message: {e}")

def on_publish(client, userdata, mid):
    logging.info(f"Published message in topic {settings.MQTT_TOPIC_SEND}")

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

def publish_message(message: dict):
    message = json.dumps(message)
    client.publish(settings.MQTT_TOPIC_SEND, message)

def unwrap_message(payload:str):
    try:
        message = json.loads(payload)
    except Exception as e:
        logging.info("Error while decoding JSON: %s", e)
        return

    logging.info(f"Received message from MQTT: {message}")

    # data unpacking (might be changed in the future)
    source_id = message.get('source_id')
    cpu_temp = message.get('cpu_temp')
    noise = message.get('noise')
    free_heap = message.get('free_heap')
    raw_packet = message.get('raw_packet')
    hop_data = message.get('hop_data')
    timestamp = message.get('timestamp')
    queue_fill = message.get('queue_fill')
    collisions = message.get('collisions')

    with get_db_session() as db:
        add_sensor_data(db, source_id, raw_packet, timestamp, noise, cpu_temp, free_heap, queue_fill, hop_data, collisions)