from core.injector import country_injector  # attribute_injector,; belong_injector,;
from fastapi import APIRouter, Depends
from schemas.gensin_schema import CreateCountrySchema
from services import CountryService

router = APIRouter(
    tags=["Country_CRUD"],
    prefix="/country"
    # dependencies = [Depends(セキュリティかトークンの設定を行う。)]
)


@router.get(
    "/get", response_model=list[CreateCountrySchema]
)  # dependencies = [Depends(セキュリティかトークンの設定を行う。)
# Dependsでスコープ認証も可能
def list_gensin(
    skip: int = 0,
    limit: int = 100,
    country_service: CountryService = Depends(country_injector(CountryService)),
):
    return country_service.get_countries_all(skip=skip, limit=limit)


@router.post("/post", response_model=CreateCountrySchema)  # Dependsでスコープ認証も可能
def create_country(
    country: CreateCountrySchema,
    country_service: CountryService = Depends(country_injector(CountryService)),
):
    country_service._is_duplicate_country(str(country.country_name))

    #         CountryService.create_country(CountryService, str(chara.country))

    #     country_id = CountryService.get_country_id(CountryService, str(chara.country))
    #     new_chara = Person.create(chara)
    #     print("test04", type(new_chara))
    # print("test01")
    return country_service.create_country(country)
