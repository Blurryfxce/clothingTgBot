from aiogram import Router

from .base_kb_handler import router as base_kb_router
from .product_kb_handler import router as carousel_kb_router

router = Router(name=__name__)

router.include_routers(
    base_kb_router,
    carousel_kb_router
)
