from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.inline.base_kb import shop_kb, categories
import database.requests as rq
from config import ADMIN_IDS

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    photo = "https://images.prom.ua/3886050239_w600_h600_3886050239.jpg"
    await message.answer_photo(
        photo=photo,
        caption=f'Congrats <b>{message.from_user.first_name}</b>! '
                f'I\'ll try to help you with finding a <i>REALLY</i> good clothing.\n\n',
        show_caption_above_media=True,
        reply_markup=shop_kb,
        parse_mode=ParseMode.HTML,
    )


@router.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer(
        text=(
            f'*Available commands:*\n'
            f'/start - Start bot\n'
            f'/help - Show this message\n'
            f'/catalog - Show the catalog\n'
            f'/about - What is the bot about?\n'
            f'/admin - List of admin commands\n'
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Command('about'))
async def handle_help(message: types.Message):
    await message.answer(
        text=(
            f'*Hi!* I was created to help you find some trendy stuff\n'
            f'Just _scroll_ through list and see by yourself - /categories\n'
        ),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Command('catalog'))
async def handle_categories(message: types.Message):
    photo = "https://jumanji.livspace-cdn.com/magazine/wp-content/uploads/2019/09/13163320/Men%E2%80%99s-Wardrobe-Design-Loft.jpg"
    await message.answer_photo(
        photo=photo,
        caption=f'Here is the catalog:',
        reply_markup=await categories(),
        parse_mode=ParseMode.HTML,
        show_caption_above_media=True,
    )


# Dealing with admin stuff
@router.message(Command('admin'))
async def handle_help(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав для цієї дії.")
        return

    await message.answer(
        text=(
            f'<b>Available admin commands:</b>\n\n'
            f'/add_item - Add new item to database\n'
            f'/clear_items - Clear Items table in database\n'
            f'/order - Confirm customer\'s order\n'
        ),
        parse_mode=ParseMode.HTML,
    )


@router.message(Command('clear_items'))
async def handle_clear_items(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав для цієї дії.")
        return

    await rq.clear_items()
    await message.answer(
        text=f'All items are cleared✅',
        parse_mode=ParseMode.HTML,
    )


class AddItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    url = State()
    photo_url = State()
    category = State()


@router.message(Command("add_item"))
async def add_item_command(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав для цієї дії.")
        return

    await message.answer("📝 Введіть назву товару:")
    await state.set_state(AddItem.name)


@router.message(AddItem.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("✏️ Введіть опис:")
    await state.set_state(AddItem.description)


@router.message(AddItem.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("💵 Введіть ціну:")
    await state.set_state(AddItem.price)


@router.message(AddItem.price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("❗ Введіть число.")
        return
    await state.update_data(price=price)
    await message.answer("🔗 Введіть URL товару:")
    await state.set_state(AddItem.url)


@router.message(AddItem.url)
async def process_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer("🖼 Введіть URL зображення:")
    await state.set_state(AddItem.photo_url)


@router.message(AddItem.photo_url)
async def process_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_url=message.text)
    await message.answer("📦 Введіть ID категорії:")
    await state.set_state(AddItem.category)


@router.message(AddItem.category)
async def process_category(message: types.Message, state: FSMContext):
    try:
        category_id = int(message.text)
    except ValueError:
        await message.answer("❗ Введіть число.")
        return

    await state.update_data(category=category_id)
    data = await state.get_data()

    await rq.set_item(
        name=data["name"],
        description=data["description"],
        url=data["url"],
        photo_url=data["photo_url"],
        price=data["price"],
        category=category_id
    )

    await message.answer("✅ Товар додано успішно!")
    await state.clear()
