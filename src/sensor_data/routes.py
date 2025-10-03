from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import Settings
from src.auth.security import get_current_token
from src.database.core import get_db
from src.sensor.connector import get_sensor_by_code
from src.sensor.exceptions import SensorNotFoundException
from src.sensor_data.connector import get_graph, get_edges, get_nodes
from src.sensor_data.models import DBSensorData
from src.sensor_data.schemas import SensorData, Graph, Edge, SensorNode

api_router = APIRouter(prefix="/sensor_data", tags=["sensor_data"])
settings = Settings()

@api_router.get("/{sensor_id}/last/graph", response_model=Graph)
async def get_latest_sensor_data_graph(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    graph = get_graph(db, sensor.last_sensor_data_id)

    return graph

@api_router.get("/{sensor_id}/last/nodes", response_model=list[SensorNode])
async def get_latest_sensor_data_nodes(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    nodes = get_nodes(db, sensor.last_sensor_data_id)

    return nodes

@api_router.get("/{sensor_id}/last/edges", response_model=list[Edge])
async def get_latest_sensor_data_edges(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    edges = get_edges(db, sensor.last_sensor_data_id)

    return edges

@api_router.get("/{sensor_id}/last/info", response_model=SensorData)
async def get_latest_sensor_data_info(sensor_id: int,
                         db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)

    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor.last_sensor_data_id).first()
    if not sensor_data:
        raise HTTPException(status_code=404, detail="No sensor data found for this sensor")

    return sensor_data
