from fastapi import HTTPException, status
from models import Belong
from repositories import BelongRepository
from schemas.gensin_schema import CreateBelongSchema

# from routers.api.country_router import CountryService


class BelongService:
    def __init__(self, belong_repository: BelongRepository) -> None:
        self._belong_repo = belong_repository

    def is_duplicate_belong(
        self,
        belong: str,
    ) -> bool:
        print("search01")
        is_duplicated = self._belong_repo.is_duplicate_belong(belong=belong)
        print("OK_10")
        if is_duplicated is True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return is_duplicated

    def get_belong_all(self, skip: int = 0, limit: int = 100) -> list[Belong]:
        print("running belongs")
        return self._belong_repo.get_all_belongs(skip=skip, limit=limit)

    def get_belong_by_id(self, belong: str) -> Belong:
        return self._belong_repo.get_belong_id(belong_name=belong)

    def create_belong(self, belong: CreateBelongSchema):
        print(belong.dict())
        new_belong = Belong(belong=belong.belong, country_id=belong.country_id)
        print("New_Belong:", new_belong)
        return self._belong_repo.create(new_belong)

    # def create_chara(self, chara: CreateGensinSchema) -> Person:
    #     print("test02")
    #     if chara.name:
    #         self._is_duplicate_name(name=chara.name)
    #     print("test03")
    #     new_chara = Person.create(chara)
    #     print("test04", type(new_chara))
    #     return self._gensin_repo.save(new_chara)


# Persons からstatusを変えることができる。
