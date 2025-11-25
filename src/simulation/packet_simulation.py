import logging

from src.sensor.models import DBClimateFrame, DBSensor
from sqlalchemy.orm import Session
from config import Settings
from sqlalchemy import and_
from datetime import datetime

settings = Settings()

def count_seconds(start: datetime, end: datetime) -> int:
    time_difference = end - start
    return int(time_difference.total_seconds())

def count_packets_for_duration(seconds: int, frequency: int) -> int:
    return seconds // frequency

def count_packets_for_period(start: datetime, end: datetime, frequency: int):
    return count_packets_for_duration(count_seconds(start,end), frequency)

def simulate_packets(db: Session,sensor_id: int, sim_start: datetime, sim_end: datetime):
    """
    calculates delivery statistics for a given sensor over a specified time period.
    :param db: database Session
    :param sensor_id: ID of the sensor to simulate packets for
    :param sim_start: datetime of simulation start
    :param sim_end: datetime of simulation end
    :return: a dictionary with simulation results
    """
    sensor_sent_packets = (db.query(DBClimateFrame).filter(and_(DBClimateFrame.sensor_id == sensor_id,
                                                                DBClimateFrame.timestamp >= int(sim_start.timestamp()),
                                                                DBClimateFrame.timestamp <= int(sim_end.timestamp()),)
                           ).count())

    total_seconds = count_seconds(sim_start, sim_end)
    desired_packets = count_packets_for_duration(total_seconds,settings.SENSOR_SEND_RATE_SECONDS)
    delivered_percent = (sensor_sent_packets / desired_packets) * 100
    delivered_mean_per_hour = sensor_sent_packets / (total_seconds/3600)

    return{
        "sensor_id": sensor_id,
        "desired_packets": desired_packets,
        "sent_packets": sensor_sent_packets,
        "delivered_percent": delivered_percent,
        "delivered_mean_per_hour": delivered_mean_per_hour
    }

def simulate_packets_all(db: Session, sim_start: datetime, sim_end: datetime):
    """
    calculates delivery statistics for all sensors over a specified time period.
    :param db: database Session
    :param sim_start: datetime of simulation start
    :param sim_end: datetime of simulation end
    :return: a dictionary with simulation results
    """
    sensor_count = db.query(DBSensor).count()
    sensor_sent_packets = (db.query(DBClimateFrame)
                           .filter(and_(DBClimateFrame.timestamp >= int(sim_start.timestamp()),
                                        DBClimateFrame.timestamp <= int(sim_end.timestamp()))
                           ).count())

    total_seconds = count_seconds(sim_start, sim_end)
    desired_packets = count_packets_for_duration(total_seconds,settings.SENSOR_SEND_RATE_SECONDS) * sensor_count
    delivered_percent = sensor_sent_packets / desired_packets * 100
    delivered_mean_per_hour = sensor_sent_packets / (total_seconds/3600)

    return{
        "sensor_count": sensor_count,
        "desired_packets": desired_packets,
        "sent_packets": sensor_sent_packets,
        "delivered_percent": delivered_percent,
        "delivered_mean_per_hour": delivered_mean_per_hour
    }