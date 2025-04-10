from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from keyboards.inline.base_kb import (
    shop_cb_data,
    categories,
)
from keyboards.inline.product_kb import build_product_kb, Products
from routers.callback_handlers.product_kb_handler import cur_page
import database.requests as rq

router = Router(name=__name__)


@router.callback_query(F.data == shop_cb_data)
async def shop_cb_handler(callback_query: CallbackQuery):
    # image_url = "https://static.wikia.nocookie.net/png-phobia/images/9/9e/Among_Drip_Killfeed.png/revision/latest/thumbnail/width/360/height/360?cb=20240511001518"
    image_url = "https://jumanji.livspace-cdn.com/magazine/wp-content/uploads/2019/09/13163320/Men%E2%80%99s-Wardrobe-Design-Loft.jpg"

    await callback_query.answer()
    await callback_query.message.answer(
        text=f'{markdown.hide_link(image_url)}Choose category:',
        reply_markup=await categories(),
        parse_mode=ParseMode.HTML,
    )


# Choose category
@router.callback_query(F.data.startswith("category_"))
async def category_cb_handler(callback_query: CallbackQuery):

    # Current page for that category resets
    category_id = int(callback_query.data.replace("category_", ""))
    user_id = callback_query.from_user.id
    cur_page[(user_id, category_id)] = 0

    items = await rq.get_items_by_category(category_id)

    if not items:
        await callback_query.message.answer("Немає товарів у цій категорії 😥")
        return

    # First item in that category
    item = items[cur_page[(user_id, category_id)]]

    markup = build_product_kb(category_id, item.url, item.id)

    await callback_query.answer()
    await callback_query.message.answer_photo(
        photo=item.photo_url,
        caption=item.name,
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )
