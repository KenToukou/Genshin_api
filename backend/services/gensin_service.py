from fastapi import HTTPException, status
from models import Person
from repositories import GensinRepository
from schemas.gensin_schema import CreateGensinSchema

# from .attribute_service import AttributeService
# from .belong_service import BelongService
# from .country_service import CountryService


class GensinService:
    def __init__(self, gensin_repository: GensinRepository) -> None:
        self._gensin_repo = gensin_repository

    def _is_duplicate_name(self, name: str, gensin_id: int | None = None) -> bool:
        is_duplicated = self._gensin_repo.is_duplicate_name(
            name=name, gensin_id=gensin_id
        )
        if is_duplicated:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return is_duplicated

    def get_chara_all(self, skip: int = 0, limit: int = 100) -> list[Person]:
        return self._gensin_repo.get_gensins(skip=skip, limit=limit)

    def get_chara_by_id(self, gensin_id: int) -> Person:
        return self._gensin_repo.get_by_id(gensin_id=gensin_id)

    def create_chara(self, chara: CreateGensinSchema) -> Person:
        if chara.name:
            self._is_duplicate_name(name=chara.name)
        new_chara = Person.create(chara=chara)
        return self._gensin_repo.save(new_chara)

    def update_charactor_info(
        self, new_info: CreateGensinSchema, charactor: Person
    ) -> None:
        return self._gensin_repo.update(chara=charactor, new_chara=new_info)

    def get_charactor_info(self, chara: Person):
        attribute = chara.get_attribute()
        belong = chara.get_belong()
        country = chara.get_country()
        return attribute, belong, country

    def delete_chara_by_id(self, id: int) -> None:
        return self._gensin_repo.delete_person_by_id(gensin_id=id)

    def get_chara_id_by_name(self, name):
        return self._gensin_repo.get_person_id(name=name)


# Persons からstatusを変えることができる。
