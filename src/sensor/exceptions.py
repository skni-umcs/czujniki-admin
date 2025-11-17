class SensorNotFoundException(Exception):
    def __init__(self):
        self.message = "No sensor with this id in the database."
        super().__init__(self.message)

class SensorIdTakenException(Exception):
    def __init__(self):
        self.message = "Sensor with this id already exists in the database."
        super().__init__(self.message)

class SensorFrequencyNotWithinLimit(Exception):
    def __init__(self):
        self.message = "Bad sensor frequency value. It should be between 5 and 3600 seconds (inclusive)."
        super().__init__(self.message)