from collections.abc import Generator

from core.database import get_session_factory
from fastapi import Depends
from schemas.auth_schema import UserInfo
from sqlalchemy.orm import Session

from .context_vars import user_info_ctx


def get_gensin_db() -> Generator[Session, None, None]:
    session_gensin = get_session_factory("gensin")
    print("DB OK")
    db = session_gensin()
    try:
        yield db
    # except Exception:
    #     db.rollback()
    #     raise
    # いずれ復活。
    finally:
        db.close()


# async def get_userinfo()-> UserInfo:


# async def set_user_info_ctx(user_info: UserInfo = Depends(get_user_info)):
#     ctx_token = user_info_ctx.set(user_info)
#     try:
#         yield user_info_ctx
#     except Exception as e:
#         raise e
#     finally:
#         user_info_ctx.reset(ctx_token)
