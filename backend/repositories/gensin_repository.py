from typing import NoReturn

from fastapi import HTTPException, status
from language import message as msg
from models import Person
from repositories.db_repository import DBRepository
from schemas.gensin_schema import CreateGensinSchema

# from sqlalchemy import BinaryExpression


class GensinRepository(DBRepository[Person]):
    def is_duplicate_name(self, name: str, gensin_id: int | None = None) -> bool:
        model_filter = Person.name == name
        if gensin_id:
            model_filter &= Person.id != gensin_id
        # binary_filter: BinaryExpression = model_filter.operator(
        #     "AND"
        # )  # model_filterをBinaryExpressionに変換
        return self._exists(model=Person, model_filter=model_filter)

    def get_person_id(self, name: str) -> int | None:
        model_filter = Person.name == name
        person = self._get(model=Person, filter=model_filter)
        print("person:", person)
        return person.id

    def get_gensins(self, skip: int = 0, limit: int = 100) -> list[Person]:
        return self._get_all(model=Person, skip=skip, limit=limit)

    def get_by_id(self, gensin_id: int, include_deleted: bool = False) -> Person:
        model_filter = Person.id == gensin_id
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        db_gensin = self._get(
            model=Person, filter=model_filter, include_deleted=include_deleted
        )
        if db_gensin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Person")),
            )
        return db_gensin

    def update(self, chara: Person, new_chara: CreateGensinSchema) -> None:
        chara.name = new_chara.name
        chara.attribute_id = new_chara.attribute_id
        chara.belong_id = new_chara.belong_id
        self._commit()

    def exists(self, gensin_id: int, include_deleted: bool = False) -> bool | NoReturn:
        model_filter = Person.id == gensin_id
        # binary_filter: BinaryExpression = model_filter.operator("AND")
        existing = self._exists(
            model=Person, model_filter=model_filter, include_deleted=include_deleted
        )
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(msg.NOT_FOUND(name="Person")),
            )
        return existing

    def save(self, person: Person) -> Person:
        person = self._merge(person)
        self._commit()
        self._reflesh(record=person)
        return person

    def delete_person_by_id(self, gensin_id: int) -> None:
        db_gensin = self.get_by_id(gensin_id=gensin_id)
        self._delete(record=db_gensin)
        self._commit()
