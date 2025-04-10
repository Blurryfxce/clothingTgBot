__all__ = ("router", )

from aiogram import Router

from .base import router as base_commands_router
from .order import router as order_commands_router
from .assistant import router as assistant_commands_router

router = Router(name=__name__)
router.include_routers(
    base_commands_router,
    order_commands_router,
    assistant_commands_router
)
