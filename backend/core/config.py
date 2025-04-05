import os
from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings

APP_NAME = os.getenv("APP_NAME", "gensin")


class BaseConfig(BaseSettings):
    default_language: Literal["en", "ja"] = "en"
    app_name: str = APP_NAME


@lru_cache
def get_config():
    return BaseConfig()


config = get_config()
