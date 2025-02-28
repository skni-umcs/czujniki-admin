class LogNotFoundException(Exception):
    def __init__(self):
        self.message = f"Log with this id doesn't exist"
        super().__init__(self.message)