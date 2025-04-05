import uuid

import routers.api as api_router
from core.context_vars import request_info_ctx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from language import message as msg
from schemas.request_info_schema import RequestInfo

app = FastAPI()
origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    try:
        request_info = RequestInfo(
            request_id=str(uuid.uuid4()),
            urlpath=request.url.path,
            method=request.method,
            remote_addr=f"{request.client.host}:{request.client.port}",  # type:ignore
            lang=request.headers.get("accept-language"),
        )
        ctx_token = request_info_ctx.set(request_info)
        response = await call_next(request)
        return response
    except Exception:
        return JSONResponse(str(msg.INTERNAL_SERVER_ERROR()), status_code=500)
    finally:
        request_info_ctx.reset(ctx_token)


app.include_router(prefix="/api", router=api_router.gensin_router)
app.include_router(prefix="/api", router=api_router.attribute_router)
app.include_router(prefix="/api", router=api_router.belong_router)
app.include_router(prefix="/api", router=api_router.country_router)
