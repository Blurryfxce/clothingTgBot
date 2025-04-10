from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum


class Products(Enum):
    shirts = 'shirts'
    pants = 'pants'
    sneakers = 'sneakers'


page_cb_prev = "page_prev"
page_cb_next = "page_next"


def build_product_kb(category_id, url, product_id) -> InlineKeyboardMarkup:
    previous_btn = InlineKeyboardButton(
        text="◀",
        callback_data=f"{page_cb_prev}:{category_id}",
    )
    download_btn = InlineKeyboardButton(
        text="Перейти на сторінку🔗",
        url=url,
    )
    next_btn = InlineKeyboardButton(
        text="▶",
        callback_data=f"{page_cb_next}:{category_id}",
    )
    order_btn = InlineKeyboardButton(
        text="🛒 Замовити",
        callback_data=f"order:{product_id}"
    )

    first_row = [previous_btn, next_btn]
    second_row = [download_btn, order_btn]
    third_row = [order_btn]

    rows = [first_row, second_row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    return markup
