from sqlalchemy.orm import Session
from .models import DBEdge, DBSensorData
from src.sensor.connector import get_sensor_by_code, update_sensor_last_sensor_data_id


def add_edge(db: Session,
             sensor_data_id: int,
             source: int,
             target: int,
             rssi: int):

    edge = DBEdge(sensor_data_id=sensor_data_id,
                  source=source,
                  target=target,
                  rssi=rssi)

    db.add(edge)

    return edge

def add_sensor_data(db: Session,
                sensor_id: int,
                raw_packet: str,
                timestamp: str,
                noise: int,
                cpu_temp: int,
                free_heap: int,
                queue_fill: int,
                path: [(int,int)],
                collisions: int) -> DBSensorData:

    hop_ids = [sensor_id]
    sensor_data = DBSensorData(sensor_id=sensor_id,
                               raw_packet=raw_packet,
                               timestamp=timestamp,
                               noise=noise,
                               cpu_temp=cpu_temp,
                               free_heap=free_heap,
                               queue_fill=queue_fill,
                               hop_ids=hop_ids,
                               collisions=collisions)

    current = sensor_id
    db.add(sensor_data)
    for (target,rssi) in path:
        sensor_data.hop_ids.append(target)
        edge = add_edge(db, sensor_data.sensor_data_id, current, target, rssi)
        sensor_data.edges.append(edge)
        current = target

    db.commit()

    update_sensor_last_sensor_data_id(db, sensor_data.sensor_id, sensor_data.sensor_data_id)

    return sensor_data

def get_graph(db: Session, sensor_data_id: int):
    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor_data_id).first()
    graph = {'nodes': [], 'edges': []}
    for ids in sensor_data.hop_ids:
        sensor = get_sensor_by_code(db, ids)
        graph['nodes'].append({
            'id': sensor.sensor_id,
            'longitude': sensor.sensor_longitude,
            'latitude': sensor.sensor_latitude,
        })
    graph['edges'] = sensor_data.edges
    return graph

def get_edges(db: Session, sensor_data_id: int):
    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor_data_id).first()
    return sensor_data.edges

def get_nodes(db: Session, sensor_data_id: int):
    sensor_data = db.query(DBSensorData).filter(DBSensorData.sensor_data_id == sensor_data_id).first()
    nodes = []
    for ids in sensor_data.hop_ids:
        sensor = get_sensor_by_code(db, ids)
        nodes.append({
            'id': sensor.sensor_id,
            'longitude': sensor.sensor_longitude,
            'latitude': sensor.sensor_latitude,
        })
    return nodes
