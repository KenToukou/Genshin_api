from typing import NoReturn

from fastapi import HTTPException, status
from language import message as msg
from models import Belong
from repositories.db_repository import DBRepository

# from sqlalchemy import BinaryExpression


class BelongRepository(DBRepository[Belong]):
    def is_duplicate_belong(
        self,
        belong: str,
    ) -> bool:
        model_filter = Belong.belong == belong

        # binary_filter: BinaryExpression = model_filter.operator(
        #     "AND"
        # )  # model_filterをBinaryExpressionに変換
        return self._exists(model=Belong, model_filter=model_filter)

    def get_all_belongs(self, skip: int = 0, limit: int = 100) -> list[Belong]:
        belongs = self._get_all(model=Belong, skip=skip, limit=limit)
        return belongs

    def get_belong_id(self, belong_name: str, include_deleted: bool = False):
        model_filter = Belong.belong == belong_name
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        db_belong = self._get(
            model=Belong, filter=model_filter, include_deleted=include_deleted
        )
        if db_belong is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Attribute")),
            )
        return db_belong.id

    def exists(self, belong_id: int, include_deleted: bool = False) -> bool | NoReturn:
        model_filter = Belong.belong_id == belong_id
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        existing = self._exists(
            model=Belong, model_filter=model_filter, include_deleted=include_deleted
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Attribute")),
            )
        return existing

    def save(self, belong: Belong) -> Belong:
        belong = self._merge(belong)
        self._commit()
        self._reflesh(record=belong)
        return belong

    def delete_belong_by_id(self, belong: str) -> None:
        db_country = self.get_belong_id(belong_name=belong)
        self._delete(record=db_country)
        self._commit()

    def create(self, belong: Belong) -> Belong:
        belong = self._create(belong)
        self._commit()
        self._reflesh(record=belong)
        return belong
