from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.frequency.models import DBFrequencyPeriod
from src.sensor_data.models import DBSensorData


def count_seconds(start: datetime, end: datetime) -> int:
    time_difference = end - start
    return int(time_difference.total_seconds())

def count_packets_for_duration(seconds: int, frequency: int) -> int:
    return seconds // frequency

def count_packets_for_period(start: datetime, end: datetime, frequency: int):
    return count_packets_for_duration(count_seconds(start,end), frequency)

def simulate_packets(db: Session,sensor_id: int, sim_start: datetime, sim_end: datetime):
    real_packets_count = db.query(DBSensorData).filter(DBSensorData.sensor_id == sensor_id,
                                                       DBSensorData.timestamp >= sim_start,
                                                       DBSensorData.timestamp <= sim_end).count()

    #TODO: check if any frequency period are in db for this sensor
    #TODO: don't count packets if frequency of a period is 0 (sensor is offline)


    best_case = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.sensor_id == sensor_id,
                                             DBFrequencyPeriod.start <= sim_start,or_(
                                            DBFrequencyPeriod.end == None,
                                            DBFrequencyPeriod.end >= sim_end)).first()

    if best_case:
        sim_packets = count_packets_for_period(sim_start, sim_end, best_case.frequency)
        return real_packets_count, sim_packets

    sum_sim_packets = 0
    current = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.sensor_id == sensor_id,
                                                           DBFrequencyPeriod.start <= sim_start,
                                                           DBFrequencyPeriod.end > sim_start).first()

    sum_sim_packets += count_packets_for_period(sim_start, current.end, current.frequency)

    current = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.sensor_id == sensor_id,
                                                 DBFrequencyPeriod.start == current.end).first()
    while current.end is not None and current.end < sim_end:
        sum_sim_packets += count_packets_for_period(current.start, current.end, current.frequency)
        current = db.query(DBFrequencyPeriod).filter(DBFrequencyPeriod.sensor_id == sensor_id,
                                                     DBFrequencyPeriod.start == current.end).first()

    sum_sim_packets += count_packets_for_period(current.start, sim_end, current.frequency)
    return real_packets_count, sum_sim_packets
