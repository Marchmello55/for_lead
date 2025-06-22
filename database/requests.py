import logging

from database.models import async_session
from database.models import User, Projects
from sqlalchemy import select, func, delete
from dataclasses import dataclass


@dataclass
class Roles:
    user: str = "user"
    admin: str = "admin"


@dataclass
class Access:
    free: str = "free"
    busy: str = "busy"


@dataclass
class state_bot:
    paid: str = "paid"
    unpaid: str = "unpaid"
    removed: str = "removed"


"""USER"""


async def get_user_tg_id(tg_id: int) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def add_new_user(data: dict) -> None:
    logging.info(f'add_new_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == int(data["tg_id"])))
        if not user:
            session.add(User(**data))
            await session.commit()


async def update_username(tg_id: int, username: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if username:
            user.username = username
        await session.commit()

async def check_user(tg_id: int):
    logging.info('check_user')
    async with  async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user: return False
        else: return True


"""BUTTON"""

"""
async def add_new_button(text: str, type_button: str) -> None:

    logging.info('add_new_button')
    async with async_session() as session:
        # Получаем максимальный существующий ID
        max_id = await session.scalar(select(func.max(Buttons.id)))

        # Определяем новый ID (если таблица пустая, начинаем с 1)
        new_id = 1 if max_id is None else max_id + 1

        # Создаем и добавляем новую кнопку
        new_button = Buttons(
            id=new_id,  # Явно указываем ID
            type_button=type_button,
            access=Access.free,
            text=text
        )

        session.add(new_button)
        await session.commit()
        logging.info(f"Добавлена новая кнопка с ID {new_id}")

async def get_button_id(id: int):
    logging.info("get_button_id")
    async with async_session() as session:
        button = await session.scalar(select(Buttons).where(Buttons.id == id))
        return button.access

async def get_buttons_type_button(type_button: str, access: str = f"{Access.free}") -> list[Buttons]:

    logging.info('get_users_type_button')
    async with async_session() as session:
        result = await session.execute(
            select(Buttons).where(Buttons.type_button == type_button).where(Buttons.access == access)
        )
        return result.scalars().all()

async def pop_access_button(text: str, type_button: str, access: str = f"{Access.busy}") -> None:
    logging.info('pop_access_button')
    async with async_session() as session:
        deleted_count = await session.execute(
            delete(Buttons)
            .where(Buttons.text == text)
            .where(Buttons.type_button == type_button)
            .where(Buttons.access == access)
        )
        await session.commit()

async def change_access_button(text: str, type_button: str, access: str = f"{Access.busy}") -> None:
    logging.info('pop_access_button')
    async with async_session() as session:
        button = await session.scalar(select(Buttons)
            .where(Buttons.text == text)
            .where(Buttons.type_button == type_button)
            .where(Buttons.access == Access.free)
        )
        button.access = access
        await session.commit()
"""

"""Projects"""


async def get_bot_id(bot_id: int):
    logging.info('get_bot_id')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        if bot: return bot
        else: return None

async def get_unpaid_bots_on_month(month: int, year: int):
    logging.info('unpaid_bots_on_month')
    async with async_session() as session:
        bots = await session.scalars(select(Projects)
            .where(Projects.paid_month < month)
            .where(Projects.paid_year < year)
            .where(Projects.state == state_bot.unpaid)
        )
        if bots:
            return [i for i in bots]
        else:
            return None

async def get_paid_bots_on_month(month: int, year: int):
    logging.info('paid_bots_on_month')
    async with async_session() as session:
        bots = await session.scalars(select(Projects)
            .where(Projects.paid_month >= month)
            .where(Projects.paid_year >= year)
            .where(Projects.state == state_bot.paid)
        )
        if bots: return [i for i in bots]
        else: return None

async def get_removed_bots_on_month(month: int, year: int):
    logging.info('paid_bots_on_month')
    async with async_session() as session:
        bots = await session.scalars(select(Projects)
            .where(Projects.paid_month <= month)
            .where(Projects.paid_year <= year)
            .where(Projects.state == state_bot.removed)
        )
        if bots: return [i for i in bots]
        else: return None

async def get_removed_bots():
    logging.info('removed_bots')
    async with async_session() as session:
        bots = await session.scalars(select(Projects)
            .where(Projects.state == state_bot.removed)
        )
        if bots:
            return [i for i in bots]
        else:
            return None

async def get_bot_id_by_name(name: str):
    logging.info("get_bot_id_by_name")
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.name == name))
        return bot

async def add_bot(name: str):
    logging.info("add_bot")
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.name == name))
        if not bot:
            session.add(Projects(name=name))
            await session.commit()

async def update_price(bot_id: int, price: str) -> None:
    logging.info('update_price')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        bot.price = price
        await session.commit()


async def update_exercise(bot_id: int, exercise: str) -> None:
    logging.info('update_exercise')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        await session.commit()
        bot.exercise = exercise


async def update_customer(bot_id: int, customer: str) -> None:
    logging.info('update_customer')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        bot.customer = customer
        await session.commit()


async def update_link_to_chat(bot_id: int, link_to_chat: str) -> None:
    logging.info('update_link_to_chat')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        bot.link_to_chat = link_to_chat
        await session.commit()


async def update_deadline(bot_id: int, deadline: str) -> None:
    logging.info('update_deadline')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        bot.deadline = deadline
        await session.commit()


async def update_executor(bot_id: int, executor: str) -> None:
    logging.info('update_executor')
    async with async_session() as session:
        bot = await session.scalar(select(Projects).where(Projects.bot_id == bot_id))
        bot.executor = executor
        await session.commit()


"""Executors"""


