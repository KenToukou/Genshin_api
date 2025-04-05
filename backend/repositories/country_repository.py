from typing import NoReturn

from fastapi import HTTPException, status
from language import message as msg
from models import Country
from repositories.db_repository import DBRepository

# from sqlalchemy import BinaryExpression


class CountryRepository(DBRepository[Country]):
    def is_duplicate_country(
        self,
        name: str,
    ) -> bool:
        print("search02")
        model_filter = Country.country_name == name

        print("search02-2:", model_filter)
        # binary_filter: BinaryExpression = model_filter.operator(
        #     "AND"
        # )  # model_filterをBinaryExpressionに変換
        return self._exists(model=Country, model_filter=model_filter)

    def get_all_countries(self, skip: int = 0, limit: int = 100) -> list[Country]:
        return self._get_all(model=Country, skip=skip, limit=limit)

    def get_country_id(self, country_name: str, include_deleted: bool = False):
        model_filter = Country.country_name == country_name
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        db_country = self._get(
            model=Country, filter=model_filter, include_deleted=include_deleted
        )
        if db_country is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Attribute")),
            )
        return db_country.id

    def exists(self, country_id: int, include_deleted: bool = False) -> bool | NoReturn:
        model_filter = Country.id == country_id
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        existing = self._exists(
            model=Country, model_filter=model_filter, include_deleted=include_deleted
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Attribute")),
            )
        return existing

    def save(self, country: Country) -> Country:
        print("test05")
        country = self._merge(country)
        print("test07")
        self._commit()
        print("test08")
        self._reflesh(record=country)
        return country

    def delete_country_by_id(self, country_name: str) -> None:
        db_country = self.get_country_id(country_name=country_name)
        self._delete(record=db_country)
        self._commit()

    def create(self, country: Country) -> Country:
        country = self._create(country)
        self._commit()
        self._reflesh(record=country)
        return country
