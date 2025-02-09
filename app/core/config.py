from typing import Optional

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    """Базовые настройки."""
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class ConfigApp(ConfigBase):
    """Настройки приложения."""
    model_config = SettingsConfigDict(env_prefix='AP_')
    title: str = Field(default='Word analitic')
    description: str = Field(default='Анализ слов')
    secret: SecretStr = Field(default='SECRET')


class ConfigDB(ConfigBase):
    """Настройки базы данных."""
    model_config = SettingsConfigDict(env_prefix='DB_')
    database_url: str = Field(default='sqlite+aiosqlite:///./fastapi.db')


class ConfigSuperUser(ConfigBase):
    """Настройки для суперюзера."""
    model_config = SettingsConfigDict(env_prefix='SU_')
    superuser_email: Optional[EmailStr] = Field(default=None)
    superuser_password: Optional[SecretStr] = Field(default=None)


class Config(BaseSettings):
    """Все настройки приложения."""
    app: ConfigApp = Field(default_factory=ConfigApp)
    db: ConfigDB = Field(default_factory=ConfigDB)
    superuser: ConfigSuperUser = Field(default_factory=ConfigSuperUser)

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config.load()
