from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SensorsAdmin"
    db_host: str = "db"
    db_port: str = "5432"
    db_user: str = "sensors"
    db_password: str = "sensors"
    db_name: str = "sensors"
    root_path: str = "/"
    KEYCLOAK_SERVER_URL: str = "https://sso.skni.umcs.pl"
    KEYCLOAK_REALM: str = "SKNI"
    KEYCLOAK_ALGO: str = "RS256"

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
