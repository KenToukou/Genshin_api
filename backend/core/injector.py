from typing import Callable

import repositories as repo
import services as sv
from fastapi import Depends
from sqlalchemy.orm import Session

from .dependencies import get_gensin_db


def gensin_injector(gensin_service: type[sv.GensinService]) -> Callable:
    get_db = get_gensin_db

    def get_service(db: Session = Depends(get_db)) -> sv.GensinService:
        return gensin_service(gensin_repository=repo.GensinRepository(db=db))

    return get_service


def attribute_injector(attribute_service: type[sv.AttributeService]) -> Callable:
    print("Attribute injector")
    get_db = get_gensin_db

    def get_service(db: Session = Depends(get_db)) -> sv.AttributeService:
        return attribute_service(attribute_repository=repo.AttributeRepository(db=db))

    return get_service


def belong_injector(belong_service: type[sv.BelongService]) -> Callable:
    get_db = get_gensin_db

    def get_service(db: Session = Depends(get_db)) -> sv.BelongService:
        return belong_service(belong_repository=repo.BelongRepository(db=db))

    return get_service


def country_injector(country_service: type[sv.CountryService]) -> Callable:
    get_db = get_gensin_db

    def get_service(db: Session = Depends(get_db)) -> sv.CountryService:
        return country_service(country_repository=repo.CountryRepository(db=db))

    return get_service
