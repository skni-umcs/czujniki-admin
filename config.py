from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SensorsAdmin"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    ROOT_PATH: str
    AUTHENTIK_SERVER_URL: str
    AUTHENTIK_APP_NAME: str
    AUTHENTIK_CLIENT_ID: str
    AUTHENTIK_ALGORITHM: str
    MQTT_CLIENT: str
    MQTT_BROKER: str
    MQTT_PORT: str
    MQTT_TOPIC_RECEIVE: str
    MQTT_TOPIC_SEND: str
    MQTT_TOPIC_CLIMATE: str
    SENSOR_OFFLINE_THRESHOLD: int
    SENSOR_SEND_RATE_SECONDS: int

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
