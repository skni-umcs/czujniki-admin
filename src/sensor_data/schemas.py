from datetime import datetime

from pydantic import BaseModel

class Edge(BaseModel):
    source: int
    target: int
    rssi: int

class SensorNode(BaseModel):
    id: int
    longitude: float
    latitude: float

class Graph(BaseModel):
    edges: list[Edge]
    nodes: list[SensorNode]

class SensorDataBase(BaseModel):
    sensor_data_id: int

class SensorDataCreate(BaseModel):
    sensor_id: int
    raw_packet: str
    timestamp: datetime
    noise: int
    cpu_temp: int
    free_heap: int
    queue_fill: int
    hop_ids: list[tuple[int, int]]
    collisions: int

class SensorData(BaseModel):
    sensor_id: int
    timestamp: datetime
    raw_packet: str
    noise: int
    cpu_temp: int
    free_heap: int
    queue_fill: int
    hop_ids: list[int]
    collisions: int

    class Config:
        from_attributes = True