from fastapi import APIRouter, Depends

from .ingest.ingest_router import router as IngestRouter
from .auth.auth_router import auth_router as AuthRouter
from .manager.manager_router import router as ManagerRouter
from .salesMan.salesMan_router import router as SalesManRouter

EndPointsRouter = APIRouter()

EndPointsRouter.include_router(IngestRouter)
EndPointsRouter.include_router(AuthRouter)
EndPointsRouter.include_router(ManagerRouter)
EndPointsRouter.include_router(SalesManRouter)
