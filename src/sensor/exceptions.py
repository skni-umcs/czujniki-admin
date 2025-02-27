class SensorNotFoundException(Exception):
    def __init__(self):
        self.message = "No sensor with this code in the database."
        super().__init__(self.message)


class SensorCodeTakenException(Exception):
    def __init__(self):
        self.message = "Sensor with this code already exists in the database."
        super().__init__(self.message)


class SensorNameTakenException(Exception):
    def __init__(self):
        self.message = "Sensor with this name already exists in the database."
        super().__init__(self.message)


class SensorLocationTakenException(Exception):
    def __init__(self):
        self.message = "There is already a sensor in this location."
        super().__init__(self.message)

