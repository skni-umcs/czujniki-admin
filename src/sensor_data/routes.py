from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import Settings
from src.database.core import get_db
from src.sensor_data.connector import add_sensor_data, get_graph, get_edges
from src.sensor_data.schemas import SensorDataWithGraph, SensorDataCreate, Graph

api_router = APIRouter(prefix="/sensor_data", tags=["sensor_data"])
settings = Settings()

@api_router.get("/{sensor_data_id}/graph", response_model=Graph)
async def get_sensor_data_graph(sensor_data_id: int,
                         db: Session = Depends(get_db)):
    graph = get_graph(db, sensor_data_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Something went wrong")
    return graph

# TODO: Only for debug, delete after all tests
@api_router.post("/", response_model=SensorDataWithGraph)
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

