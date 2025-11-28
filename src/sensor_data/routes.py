from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import Settings
from src.auth.security import get_current_token
from src.database.core import get_db
from src.sensor.connector import get_sensor_by_id, get_all_sensors
from src.sensor.exceptions import SensorNotFoundException
from src.sensor_data.connector import get_graph, get_edges, get_nodes
from src.sensor_data.models import DBSensorData
from src.sensor_data.schemas import SensorData, Graph, Edge, SensorNode

api_router = APIRouter(prefix="/sensor_data", tags=["sensor_data"])
settings = Settings()

@api_router.get("/last/info", response_model=list[SensorData])
async def get_all_latest_sensor_data_info(db: Session = Depends(get_db), token = Depends(get_current_token)):
    sensor_data_list = []
    sensors = get_all_sensors(db)

    for sensor in sensors:

        sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor.last_sensor_data_id).first()
        if sensor_data:
            sensor_data_list.append({
                "sensor_id": sensor_data.sensor_id,
                "timestamp": sensor_data.timestamp,
                "raw_packet": sensor_data.raw_packet,
                "noise": sensor_data.noise,
                "cpu_temp": sensor_data.cpu_temp,
                "free_heap": sensor_data.free_heap,
                "longitude": sensor.sensor_longitude,
                "latitude": sensor.sensor_latitude,
                "queue_fill": sensor_data.queue_fill,
                "hop_ids": sensor_data.hop_ids,
                "collisions": sensor_data.collisions
            })

    return sensor_data_list

@api_router.get("/{sensor_id}/last/graph", response_model=Graph)
async def get_latest_sensor_data_graph(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_id(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    graph = get_graph(db, sensor.last_sensor_data_id)

    return graph

@api_router.get("/{sensor_id}/last/nodes", response_model=list[SensorNode])
async def get_latest_sensor_data_nodes(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_id(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    nodes = get_nodes(db, sensor.last_sensor_data_id)

    return nodes

@api_router.get("/{sensor_id}/last/edges", response_model=list[Edge])
async def get_latest_sensor_data_edges(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_id(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    edges = get_edges(db, sensor.last_sensor_data_id)

    return edges

@api_router.get("/{sensor_id}/last/info", response_model=SensorData)
async def get_latest_sensor_data_info(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_id(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)

    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor.last_sensor_data_id).first()
    if not sensor_data:
        raise HTTPException(status_code=404, detail="No sensor data found for this sensor")

    response = {
        "sensor_id": sensor_data.sensor_id,
        "timestamp": sensor_data.timestamp,
        "raw_packet": sensor_data.raw_packet,
        "noise": sensor_data.noise,
        "cpu_temp": sensor_data.cpu_temp,
        "free_heap": sensor_data.free_heap,
        "longitude": sensor.sensor_longitude,
        "latitude": sensor.sensor_latitude,
        "queue_fill": sensor_data.queue_fill,
        "hop_ids": sensor_data.hop_ids,
        "collisions": sensor_data.collisions
    }

    return response
