from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_categories

shop_cb_data = "shop"
shirts_cb_data = "shirts"
pants_cb_data = "pants"
sneakers_cb_data = "sneakers"


shop_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Shop🛒",
        callback_data=shop_cb_data,
        parse_mode=ParseMode.HTML,
    )]
])


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    return keyboard.adjust(1).as_markup()

