from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SensorsAdmin"
    db_host: str = "db"
    db_port: str = "5432"
    db_user: str = "sensors"
    db_password: str = "sensors"
    db_name: str = "sensors"
    root_path: str = "/"
    KEYCLOAK_SERVER_URL: str = "keycloak-root-url"
    KEYCLOAK_REALM: str = "realm-name"
    KEYCLOAK_CLIENT_ID: str = "client-id"
    KEYCLOAK_CLIENT_SECRET: str = "client-secret"

    # "account" worked, but I don't know where to get info about this
    # value other than the token itself.
    KEYCLOAK_AUDIENCE: str = "keycloak-audience"

    KEYCLOAK_ALGO: str = "keycloak-algorithm"

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
