from paho.mqtt import client as mqtt
from config import Settings
import logging
import json
import asyncio
from src.database.core import get_db_session
from src.sensor_data.connector import add_sensor_data
from src.sensor.connector import update_sensor_on_ping, create_new_climate_frame, update_sensor_last_sensor_data_id
from src.websockets.utils import push_sensor_update, push_service_update
import src.shared_state as state

settings = Settings()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, settings.MQTT_CLIENT)

def on_connect(client, userdata, flags, rc):

    logging.info(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(settings.MQTT_TOPIC_SEND)
    client.subscribe(settings.MQTT_TOPIC_RECEIVE)
    client.subscribe(settings.MQTT_TOPIC_CLIMATE)
    logging.info(f"MQTT client is now listening for messages...")

def on_message(client, userdata, msg):

    if msg.topic != settings.MQTT_TOPIC_RECEIVE and msg.topic != settings.MQTT_TOPIC_CLIMATE:
        return
    try:
        handle_message(msg)

        if state.MAIN_EVENT_LOOP:
            state.MAIN_EVENT_LOOP.call_soon_threadsafe(
                lambda: asyncio.create_task(push_sensor_update())
            )

    except RuntimeError as re:
        logging.error(f"Runtime error while pushing websocket update: {re}")
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

def handle_message(msg):

    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
    except Exception as e:
        logging.info("Error while decoding JSON: %s", e)
        return
    if msg.topic == settings.MQTT_TOPIC_CLIMATE:
        handle_new_climate_data(data)
    else:
        handle_new_service_data(data)

def handle_new_climate_data(data:dict):

    sensor_id = data.get('sensor_id')
    timestamp = int(data.get('time'))
    logging.info(f"Received climate data from sensor {sensor_id} at time {timestamp}")

    with get_db_session() as db:
        update_sensor_on_ping(db, sensor_id, timestamp, "climate")
        create_new_climate_frame(db, sensor_id, timestamp)

def handle_new_service_data(data:dict):

    source_id = data.get('source_id')
    cpu_temp = data.get('cpu_temperature')
    noise = data.get('noise')
    free_heap = data.get('free_heap')
    raw_packet = data.get('raw_packet')
    hop_data = data.get('hop_data')
    timestamp = int(data.get('timestamp'))
    queue_fill = data.get('queue_fill')
    collisions = data.get('collision_rate')

    with get_db_session() as db:
        update_sensor_on_ping(db, source_id, timestamp, "service")
        add_sensor_data(db, source_id, raw_packet, timestamp, noise, cpu_temp, free_heap, queue_fill, hop_data, collisions)

    if state.MAIN_EVENT_LOOP:
        state.MAIN_EVENT_LOOP.call_soon_threadsafe(
            lambda: asyncio.create_task(push_service_update(source_id))
        )