from contextvars import ContextVar

from schemas.auth_schema import UserInfo
from schemas.request_info_schema import RequestInfo

request_info_ctx: ContextVar[RequestInfo | None] = ContextVar(
    "request_info_ctx", default=None
)
user_info_ctx: ContextVar[UserInfo | None] = ContextVar("user_info_ctx")


def get_current_user() -> str | None:
    user_info = user_info_ctx.get()
    if user_info:
        return f"{user_info.name}"
    return "Gensin"


def get_current_user_info() -> UserInfo | None:
    return user_info_ctx.get()


def get_request_id() -> str | None:
    request_info = request_info_ctx.get()
    if request_info:
        return request_info.request_id
    return None


def get_request_urlpath() -> str | None:
    request_info = request_info_ctx.get()
    if request_info:
        return request_info.urlpath
    return None


def get_request_method() -> str | None:
    request_info = request_info_ctx.get()
    if request_info:
        return request_info.method
    return None


def get_request_lang() -> str | None:
    request_info = request_info_ctx.get()
    if request_info:
        return request_info.lang
    return None
