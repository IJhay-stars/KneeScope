import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from knee_api.config import settings
from knee_api.routers import exams, health, predict

logger = logging.getLogger("knee_api")


def create_app() -> FastAPI:
    logging.basicConfig(
        level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    app = FastAPI(title="Knee MRI Triage API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        rid = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
        response = await call_next(request)
        response.headers["x-request-id"] = rid
        logger.info("%s %s -> %s [%s]", request.method, request.url.path, response.status_code, rid)
        return response

    app.include_router(health.router)
    app.include_router(exams.router, prefix="/v1")
    app.include_router(predict.router, prefix="/v1")
    return app


app = create_app()
