from aiogram import Router, F, types
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from collections import defaultdict

from database.requests import get_items_by_category

from keyboards.inline.product_kb import (
    build_product_kb,
    page_cb_prev,
    page_cb_next,
)

router = Router(name=__name__)


cur_page = defaultdict(int)


@router.callback_query(F.data.startswith("page"))
async def update_page_callback_handler(callback_query: CallbackQuery):
    action, category_id = callback_query.data.split(":")
    user_id = callback_query.from_user.id

    key = (user_id, int(category_id))

    if action == page_cb_prev:
        cur_page[key] -= 1
    else:
        cur_page[key] += 1

    page_index = cur_page[key]
    item = await get_item(category_id, page_index)

    markup = build_product_kb(category_id, item.url, item.id)

    await callback_query.answer()
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=await update_photo(category_id, page_index),
            caption=item.name,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=markup,
    )


async def update_caption(category_id: int, page: int):
    items = await get_items_by_category(category_id)
    item_name = items[page % len(items)].name

    return item_name


async def update_photo(category_id: int, page: int):
    items = await get_items_by_category(category_id)
    photo_url = items[page % len(items)].photo_url

    return photo_url


async def get_item(category_id: int, page: int):
    items = await get_items_by_category(category_id)
    item = items[page % len(items)]

    return item



