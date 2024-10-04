class ModuleNotFoundException(Exception):
    def __init__(self):
        self.message = "No module with this code in the database."
        super().__init__(self.message)


class ModuleCodeTakenException(Exception):
    def __init__(self):
        self.message = "Module with this code already exists in the database."
        super().__init__(self.message)


class ModuleNameTakenException(Exception):
    def __init__(self):
        self.message = "Module with this name already exists in the database."
        super().__init__(self.message)


class LocationTakenException(Exception):
    def __init__(self):
        self.message = "There is already a module in this location."
        super().__init__(self.message)


class ReceivedRSSIFromNotActiveModuleException(Exception):
    def __init__(self):
        self.message = "Received RSSI from module marked as inactive."
        super().__init__(self.message)


class BadDateTimeFormatException(Exception):
    def __init__(self):
        self.message = "Bad date-time format. Use %Y-%m-%d %H:%M:%S format."
        super().__init__(self.message)
