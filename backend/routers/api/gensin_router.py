import pandas as pd
from core.injector import (  # attribute_injector,; belong_injector,; country_injector,
    gensin_injector,
)
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas.gensin_schema import CreateGensinSchema, DeleteGensin, ShowPerson
from services import GensinService

router = APIRouter(
    tags=["Gensin_CRUD"],
    prefix="/gensin"
    # dependencies = [Depends(セキュリティかトークンの設定を行う。)]
)

templates = Jinja2Templates(directory="static")


@router.get(
    "/get", response_model=list[ShowPerson]
)  # dependencies = [Depends(セキュリティかトークンの設定を行う。)
# Dependsでスコープ認証も可能
async def list_gensin(
    skip: int = 0,
    limit: int = 100,
    gensin_service: GensinService = Depends(gensin_injector(GensinService)),
):
    return gensin_service.get_chara_all(skip=skip, limit=limit)


@router.get("/get_DataFrame", response_class=HTMLResponse)
async def show_and_save_data_frame(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    gensin_service: GensinService = Depends(gensin_injector(GensinService)),
):
    name_list: list = []
    attribute_list: list = []
    belong_list: list = []
    country_list: list = []
    charactors = gensin_service.get_chara_all(skip=skip, limit=limit)
    for charactor in charactors:
        attribute, belong, country = gensin_service.get_charactor_info(charactor)
        name_list.append(charactor.name)
        attribute_list.append(attribute)
        belong_list.append(belong)
        country_list.append(country)
    df_charactor = pd.DataFrame(
        data={
            "名前": name_list,
            "属性": attribute_list,
            "所属": belong_list,
            "国": country_list,
        }
    )
    print(df_charactor)
    df_charactor.to_csv("temp/test.csv", index=False)
    table = df_charactor.to_html(
        index=False,
        justify="center",
        classes="table table-bordered table-striped table-hover",
    )
    return templates.TemplateResponse(
        "index.html", {"request": request, "table": table}
    )


@router.get("/get_id_by/{name}")
async def get_id_by_name(
    name: str, gensin_service: GensinService = Depends(gensin_injector(GensinService))
) -> int:
    return gensin_service.get_chara_id_by_name(name=name)


@router.post("/post", response_model=ShowPerson)  # Dependsでスコープ認証も可能
async def create_chara(
    chara: CreateGensinSchema,
    gensin_service: GensinService = Depends(gensin_injector(GensinService)),
):
    return gensin_service.create_chara(chara=chara)


@router.post("/{id}/post", response_model=ShowPerson)
async def modify_charactor_infomation(
    id: int,
    new_chara: CreateGensinSchema,
    gensin_service: GensinService = Depends(gensin_injector(GensinService)),
):
    charactor = gensin_service.get_chara_by_id(id)
    # new_charactor_info = gensin_service.create_chara(chara)
    gensin_service.update_charactor_info(new_info=new_chara, charactor=charactor)
    print("Registered")
    return None


@router.delete("/delete_name")  # Dependsでスコープ認証も可能
async def delete_chara(
    chara_name: DeleteGensin,
    gensin_service: GensinService = Depends(gensin_injector(GensinService)),
):
    chara_id = gensin_service.get_chara_id_by_name(chara_name.name)
    return gensin_service.delete_chara_by_id(chara_id)
