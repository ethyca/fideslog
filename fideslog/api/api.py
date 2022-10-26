from fastapi import APIRouter
from fideslog.api.endpoints.events import event_router
from fideslog.api.endpoints.health import health_router

api_router = APIRouter()
api_router.include_router(event_router)
api_router.include_router(health_router)