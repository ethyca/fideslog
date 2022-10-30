from fastapi import APIRouter

from fideslog.api.routes.events import event_router
from fideslog.api.routes.health import health_router
from fideslog.api.routes.registrations import registration_router

api_router = APIRouter()
api_router.include_router(event_router)
api_router.include_router(health_router)
api_router.include_router(registration_router)
