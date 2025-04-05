from typing import Generic, TypeVar

from core.database import Base
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression

_T = TypeVar("_T", bound=Base)


class DBRepository(Generic[_T]):
    def __init__(self, db: Session) -> None:
        self._db = db

    def _get_all(
        self,
        model: type[_T],
        filter: BinaryExpression | None = None,
        skip: int = 0,
        limit: int = 100,
        order_by_desc: bool = True,
        order_by_column="id",
        include_deleted: bool = False,
    ) -> list[_T]:
        query = self._db.query(model)
        if filter is not None:
            query = query.filter(filter)
        if include_deleted:
            query = query.execution_options(include_deleted=True)
        if order_by_desc:
            query = query.order_by(getattr(model, order_by_column).desc())
        else:
            query = query.order_by(getattr(model, order_by_column).abc())
        if limit:
            query = query.limit(limit).offset(skip)
        return query.all()

    def _get(
        self,
        model: type[_T],
        filter: BinaryExpression | None = None,
        include_deleted: bool = False,
    ) -> _T | None:
        query = self._db.query(model)
        if filter is not None:
            query = query.filter(filter)
        if include_deleted:
            query = query.execution_options(include_deleted=True)
        return query.one_or_none()

    def _create(self, record: _T) -> _T:
        self._db.add(record)
        return record

    def _merge(self, record: _T) -> _T:
        return self._db.merge(record)

    def _delete(self, record: _T) -> None:
        self._db.delete(record)

    def _exists(
        self,
        model: type[_T],
        model_filter: BinaryExpression | None = None,
        include_deleted: bool = False,
    ) -> bool:
        query = self._db.query(model)
        if model_filter is not None:
            query = query.filter(model_filter)
        if include_deleted:
            query = query.execution_options(include_deleted=True)
        exists: bool = self._db.query(query.exists()).scalar()
        return exists

    def _commit(self) -> None:
        self._db.commit()

    def _reflesh(self, record: _T) -> None:
        self._db.refresh(record)
