from database.models import async_session
from database.models import User, Category, Item, Order
from sqlalchemy import select, update, delete


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()


async def set_item(name, description, url, photo_url, price, category):
    async with async_session() as session:
        session.add(Item(
            name=name,
            description=description,
            url=url, photo_url=photo_url,
            price=price,
            category=category))
        await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_items_by_category(category_id: int) -> list[Item]:
    async with async_session() as session:
        result = await session.scalars(
            select(Item).where(Item.category == category_id)
        )
        return result.all()


async def get_item_by_id(item_id: int) -> Item:
    async with async_session() as session:
        item = await session.get(Item, item_id)

        return item


async def clear_items():
    async with async_session() as session:
        await session.execute(delete(Item))
        await session.commit()


async def set_order(user_name, product_name, quantity):
    async with async_session() as session:
        session.add(Order(
            username=user_name,
            product_name=product_name,
            quantity=quantity,
            ))
        await session.commit()
