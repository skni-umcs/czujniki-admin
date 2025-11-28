from pydantic import BaseModel

class Edge(BaseModel):
    id: int
    source: int
    target: int
    dbm: int
    rssi: int

class SensorNode(BaseModel):
    id: int
    source: int
    target: int
    longitude: float
    latitude: float
    stat1: int

class Graph(BaseModel):
    edges: list[Edge]
    nodes: list[SensorNode]
    timestamp: str

class SensorDataBase(BaseModel):
    sensor_data_id: int

class SensorDataCreate(BaseModel):
    sensor_id: int
    raw_packet: str
    timestamp: int
    noise: int
    cpu_temp: int
    free_heap: int
    queue_fill: int
    hop_ids: list[tuple[int, int]]
    collisions: int

class SensorData(BaseModel):
    sensor_id: int
    timestamp: int
    raw_packet: str
    noise: int
    cpu_temp: int
    free_heap: int
    queue_fill: int
    hop_ids: list[tuple[int, int]]
    collisions: int | None

    class Config:
        from_attributes = True