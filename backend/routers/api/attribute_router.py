from core.injector import attribute_injector
from fastapi import APIRouter, Depends
from schemas.gensin_schema import CreateAttributeSchema
from services import AttributeService

router = APIRouter(
    tags=["Attribute_CRUD"],
    prefix="/attribute"
    # dependencies = [Depends(セキュリティかトークンの設定を行う。)]
)


@router.get(
    "/get", response_model=list[CreateAttributeSchema]
)  # dependencies = [Depends(セキュリティかトークンの設定を行う。)
# Dependsでスコープ認証も可能
def list_attributes(
    skip: int = 0,
    limit: int = 100,
    attribute_service: AttributeService = Depends(attribute_injector(AttributeService)),
):
    return attribute_service.get_attribute_all(skip=skip, limit=limit)


@router.post("/post", response_model=CreateAttributeSchema)  # Dependsでスコープ認証も可能
def create_chara(
    attribute: CreateAttributeSchema,
    attribute_service: AttributeService = Depends(attribute_injector(AttributeService)),
):
    print("Attribute")
    return attribute_service.create_attribute(attribute=attribute)
