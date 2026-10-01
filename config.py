from psycopg.conninfo import make_conninfo
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    greeting: str = "Добро пожаловать в гостевую книгу!"

    db_host: str = "localhost"
    db_port: int = 5432
    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str

    @property
    def database_conninfo(self) -> str:
        return make_conninfo(
            host=self.db_host,
            port=self.db_port,
            user=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            dbname=self.postgres_db,
        )


settings = Settings()
