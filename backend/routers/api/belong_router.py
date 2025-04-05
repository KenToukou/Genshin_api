from core.injector import belong_injector  # attribute_injector,; ; country_injector,
from fastapi import APIRouter, Depends
from schemas.gensin_schema import CreateBelongSchema, ShowBelong
from services import BelongService

router = APIRouter(
    tags=["Belong_CRUD"],
    prefix="/belong"
    # dependencies = [Depends(セキュリティかトークンの設定を行う。)]
)


@router.get(
    "/get", response_model=list[CreateBelongSchema]
)  # dependencies = [Depends(セキュリティかトークンの設定を行う。)
# Dependsでスコープ認証も可能
def list_belongs(
    skip: int = 0,
    limit: int = 100,
    belong_service: BelongService = Depends(belong_injector(BelongService)),
):
    print("Start belongs")
    return belong_service.get_belong_all(skip=skip, limit=limit)


@router.post("/post", response_model=ShowBelong)  # Dependsでスコープ認証も可能
def create_belong(
    belong: CreateBelongSchema,
    belong_service: BelongService = Depends(belong_injector(BelongService)),
):
    belong_service.is_duplicate_belong(belong.belong)
    return belong_service.create_belong(belong=belong)
