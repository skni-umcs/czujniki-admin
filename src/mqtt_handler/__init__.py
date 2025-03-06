from paho.mqtt import client as mqtt
from config import Settings
import logging
import json
from src.database.core import get_db_session
from src.sensor.connector import update_sensor_data

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
        logging.info(e)
        return

    logging.info(f"Received message: {message}")

    # keys might finally be different, keep in mind
    sensor_code = message.get('sensor_id')
    new_rssi = message.get('rssi')
    new_cpu_temp = message.get('cpu_temp')
    new_sensor_noise = message.get('sensor_noise')

    with get_db_session() as db:
        update_sensor_data(db,sensor_code,new_rssi,new_cpu_temp,new_sensor_noise)


