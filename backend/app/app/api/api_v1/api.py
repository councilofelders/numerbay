from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    categories,
    globals,
    items,
    login,
    models,
    numerai,
    products,
    scheduler,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(numerai.router, prefix="/numerai", tags=["numerai"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["scheduler"])
api_router.include_router(globals.router, prefix="/globals", tags=["globals"])
