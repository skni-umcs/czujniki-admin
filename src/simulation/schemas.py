from pydantic import BaseModel

class AllSimulationResponseSchema(BaseModel):
    sensor_count: int
    desired_packets: int
    sent_packets: int
    delivered_percent: float
    delivered_mean_per_hour: float

class SimulationResponseSchema(BaseModel):
    sensor_id: int
    desired_packets: int
    sent_packets: int
    delivered_percent: float
    delivered_mean_per_hour: float