from typing import NoReturn

from fastapi import HTTPException, status
from language import message as msg
from models import Attribute
from repositories.db_repository import DBRepository

# from sqlalchemy import BinaryExpression


class AttributeRepository(DBRepository[Attribute]):
    def is_duplicate_attribute(
        self,
        name: str,
    ) -> bool:
        print("search02")
        model_filter = Attribute.attribute_name == name

        print("search02-2:", model_filter)
        # binary_filter: BinaryExpression = model_filter.operator(
        #     "AND"
        # )  # model_filterをBinaryExpressionに変換
        return self._exists(model=Attribute, model_filter=model_filter)

    def get_all_attributes(self, skip: int = 0, limit: int = 100) -> list[Attribute]:
        return self._get_all(model=Attribute, skip=skip, limit=limit)

    def get_attribute_id(self, attribute_name: str, include_deleted: bool = False):
        model_filter = Attribute.attribute_name == attribute_name
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        db_attribute = self._get(
            model=Attribute, filter=model_filter, include_deleted=include_deleted
        )
        if db_attribute is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Attribute")),
            )
        return db_attribute.id

    def exists(
        self, attribute_id: int, include_deleted: bool = False
    ) -> bool | NoReturn:
        model_filter = Attribute.id == attribute_id
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        existing = self._exists(
            model=Attribute, model_filter=model_filter, include_deleted=include_deleted
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Attribute")),
            )
        return existing

    def save(self, attribute: Attribute) -> Attribute:
        print("test05")
        attribute = self._merge(attribute)
        print("test07")
        self._commit()
        print("test08")
        self._reflesh(record=attribute)
        return attribute

    def delete_attribute_by_id(self, attribute_name: str) -> None:
        db_attribute = self.get_attribute_id(attribute_name=attribute_name)
        self._delete(record=db_attribute)
        self._commit()

    def create(self, attribute: Attribute) -> Attribute:
        attribute = self._create(attribute)
        self._commit()
        self._reflesh(record=attribute)
        return attribute
