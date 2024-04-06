from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

MONGO_DSN_TEMPLATE = "mongodb://{host}:{port}/{database}"


class MongoSettings(BaseModel):
    HOST: str
    PORT: int
    DATABASE: str

    @property
    def url(self) -> str:
        return MONGO_DSN_TEMPLATE.format(
            host=self.HOST,
            port=self.PORT,
            database=self.DATABASE,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    mongo: MongoSettings
