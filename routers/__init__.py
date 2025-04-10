__all__ = ("router", )

from aiogram import Router

from .commands import router as commands_router
from .callback_handlers import router as callback_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    callback_router
)
