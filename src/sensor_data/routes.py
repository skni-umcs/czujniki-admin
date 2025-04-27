from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import Settings
from src.database.core import get_db
from src.sensor.connector import get_sensor_by_code, update_sensor_last_sensor_data_id
from src.sensor.exceptions import SensorNotFoundException
from src.sensor_data.connector import add_sensor_data, get_graph, get_edges, get_nodes
from src.sensor_data.schemas import SensorData, SensorDataCreate, Graph, Edge, SensorNode

api_router = APIRouter(prefix="/sensor_data", tags=["sensor_data"])
settings = Settings()

# TODO: This route is only for debug, newer use in prod, delete after full MQTT integration
@api_router.post("/", response_model=SensorData)
async def add_sensor_data_route(sensor_data: SensorDataCreate,
                                 db: Session = Depends(get_db)):
    try:
        sensor_data = add_sensor_data(db, sensor_data.sensor_id, sensor_data.raw_packet,
                                      sensor_data.timestamp, sensor_data.noise,
                                      sensor_data.cpu_temp, sensor_data.free_heap,
                                      sensor_data.queue_fill, sensor_data.hop_ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return sensor_data

@api_router.get("/{sensor_id}/last/graph", response_model=Graph)
async def get_latest_sensor_data_graph(sensor_id: int,
                         db: Session = Depends(get_db)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    graph = get_graph(db, sensor.last_sensor_data_id)

    return graph

@api_router.get("/{sensor_id}/last/nodes", response_model=list[SensorNode])
async def get_latest_sensor_data_nodes(sensor_id: int,
                         db: Session = Depends(get_db)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    nodes = get_nodes(db, sensor.last_sensor_data_id)

    return nodes

@api_router.get("/{sensor_id}/last/edges", response_model=list[Edge])
async def get_latest_sensor_data_edges(sensor_id: int,
                         db: Session = Depends(get_db)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException:
        raise SensorNotFoundException

    edges = get_edges(db, sensor.last_sensor_data_id)

    return edges
