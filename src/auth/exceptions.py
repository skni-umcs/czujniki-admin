class CredentialsException(Exception):
    def __init__(self, message: str = "Error validating credentials") -> None:
        super().__init__(message)