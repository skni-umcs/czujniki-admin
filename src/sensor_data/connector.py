from datetime import datetime

from sqlalchemy.orm import Session
from .models import DBEdge, DBSensorData
from src.sensor.connector import get_sensor_by_id, update_sensor_last_sensor_data_id


def add_edge(db: Session,
             path_id: int,
             sensor_data_id: int,
             source: int,
             target: int,
             rssi: int):

    edge = DBEdge(sensor_data_id=sensor_data_id,
                  id=path_id,
                  source=source,
                  target=target,
                  rssi=rssi,
                  dbm=-(256 - rssi))

    db.add(edge)

    return edge

def add_sensor_data(db: Session,
                sensor_id: int,
                raw_packet: str,
                timestamp: int,
                noise: int,
                cpu_temp: int,
                free_heap: int,
                queue_fill: int,
                hop_data: [(int,int)],
                collisions: int) -> DBSensorData:

    sensor_data = DBSensorData(sensor_id=sensor_id,
                               raw_packet=raw_packet,
                               timestamp=timestamp,
                               noise=noise,
                               cpu_temp=cpu_temp,
                               free_heap=free_heap,
                               queue_fill=queue_fill,
                               hop_ids=hop_data,
                               collisions=collisions)

    current = sensor_id
    db.add(sensor_data)
    for i, (target, rssi) in enumerate(hop_data):
        edge = add_edge(db, i, sensor_data.sensor_data_id, current, target, rssi)
        sensor_data.edges.append(edge)
        current = target

    db.commit()

    update_sensor_last_sensor_data_id(db, sensor_data.sensor_id, sensor_data.sensor_data_id)

    return sensor_data

def get_graph(db: Session, sensor_data_id: int):
    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor_data_id).first()
    graph = {'nodes': [], 'edges': [],'timestamp': str(datetime.fromtimestamp(sensor_data.timestamp))}
    for edge in sensor_data.edges:
        sensor_info = get_sensor_by_id(db, edge.source)
        graph['nodes'].append({
            'id': sensor_info.sensor_id,
            'source': edge.source,
            'target': edge.target,
            'longitude': sensor_info.sensor_longitude,
            'latitude': sensor_info.sensor_latitude,
            'stat1': edge.dbm
        })
        graph['edges'].append({
            'id': edge.id,
            'source': edge.source,
            'target': edge.target,
            'dbm': edge.dbm,
            'rssi': edge.rssi
        })
    return graph

def get_edges(db: Session, sensor_data_id: int):
    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor_data_id).first()
    return sensor_data.edges

def get_nodes(db: Session, sensor_data_id: int):
    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor_data_id).first()
    nodes = []
    for edge in sensor_data.edges:
        sensor_info = get_sensor_by_id(db, edge.source)
        nodes.append({
            'id': sensor_info.sensor_id,
            'source': edge.source,
            'target': edge.target,
            'longitude': sensor_info.sensor_longitude,
            'latitude': sensor_info.sensor_latitude,
            'stat1': edge.dbm
        })
    return nodes
