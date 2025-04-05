from pydantic import BaseModel as PydanticBaseModel


class RequestInfo(PydanticBaseModel):
    request_id: str | None
    urlpath: str | None
    method: str | None
    remote_addr: str | None
    lang: str | None
