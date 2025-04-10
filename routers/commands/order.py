from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from config import ADMIN_IDS
import database.requests as rq


router = Router(name=__name__)


class OrderStates(StatesGroup):
    waiting_for_quantity = State()
    waiting_for_confirm = State()


def quantity_kb():
    buttons = [InlineKeyboardButton(text=str(i), callback_data=f"qty:{i}") for i in range(1, 6)]
    rows = [[btn] for btn in buttons]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirm_order_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm_order"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_order")
        ]
    ])


# Order callbacks
@router.callback_query(F.data.startswith("order:"))
async def handle_order_start(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split(":", 1)[1])
    item = await rq.get_item_by_id(item_id)

    await state.update_data(product_name=item.name, item_id=item_id)
    await state.set_state(OrderStates.waiting_for_quantity)
    await callback.message.answer(f"Оберіть кількість для: <b>{item.name}</b>", reply_markup=quantity_kb(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("qty:"))
async def handle_quantity_selected(callback: CallbackQuery, state: FSMContext):
    quantity = int(callback.data.split(":")[1])
    await state.update_data(quantity=quantity)
    data = await state.get_data()
    await state.set_state(OrderStates.waiting_for_confirm)

    await callback.message.answer(
        f"Підтвердіть замовлення:\n\n📦 <b>{data['product_name']}</b>\n🔢 Кількість: {quantity}",
        reply_markup=confirm_order_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_order")
async def handle_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    username = callback.from_user.username or f"id:{callback.from_user.id}"
    product = data["product_name"]
    qty = data["quantity"]

    ADMIN_ID = ADMIN_IDS[0]
    await callback.bot.send_message(
        ADMIN_ID,
        f"<b>НОВЕ ЗАМОВЛЕННЯ</b>\n👤 @{username}\n📦 {product}\n🔢 Кількість: {qty}",
        parse_mode="HTML"
    )
    await callback.message.answer("✅ Замовлення надіслано адміністратору!")
    await callback.answer()


@router.callback_query(F.data == "cancel_order")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Замовлення скасовано.")
    await callback.answer()


# Admin side
@router.message(Command("order"))
async def admin_confirm_order(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав для цієї дії.")
        return

    if not message.reply_to_message:
        await message.answer("⚠️ Ви повинні відповісти на повідомлення з замовленням.")
        return

    lines = message.reply_to_message.text.split("\n")

    try:
        username_line = lines[1].strip()
        product_line = lines[2].strip()
        quantity_line = lines[3].strip()

        username = username_line.split("@")[1]

        product_name = product_line[2:].strip()

        quantity = int(quantity_line.split(":")[1].strip())

        await rq.set_order(username, product_name, quantity)
        await message.answer("✅ Замовлення збережено в базі.")
    except (IndexError, ValueError):
        await message.answer(
            "⚠️ Невірний формат повідомлення. Переконайтесь, що ви відповідаєте на правильне повідомлення.")
