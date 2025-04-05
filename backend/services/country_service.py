from fastapi import HTTPException, status
from models import Country
from repositories import CountryRepository
from schemas.gensin_schema import CreateCountrySchema


class CountryService:
    def __init__(self, country_repository: CountryRepository) -> None:
        self._country_repo = country_repository

    def _is_duplicate_country(
        self,
        country_name: str,
    ) -> bool:
        print("search01")
        is_duplicated = self._country_repo.is_duplicate_country(name=country_name)
        print("OK_10")
        print(is_duplicated)
        if is_duplicated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return is_duplicated

    def get_countries_all(self, skip: int = 0, limit: int = 100) -> list[Country]:
        return self._country_repo.get_all_countries(skip=skip, limit=limit)

    def get_country_id(self, country_name: str):
        return self._country_repo.get_country_id(country_name=country_name)

    def create_country(self, country: CreateCountrySchema):
        print(country.dict())
        new_country = Country(country_name=country.country_name)
        return self._country_repo.create(new_country)

    # def create_chara(self, chara: CreateGensinSchema) -> Person:
    #     print("test02")
    #     if chara.name:
    #         self._is_duplicate_name(name=chara.name)
    #     print("test03")
    #     new_chara = Person.create(chara)
    #     print("test04", type(new_chara))
    #     return self._gensin_repo.save(new_chara)


# Persons からstatusを変えることができる。
