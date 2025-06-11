import logging

from database.models import async_session
from database.models import User, Buttons, Progects
from sqlalchemy import select, func, delete
from dataclasses import dataclass


@dataclass
class Roles:
    user: str = "user"
    admin: str = "admin"


@dataclass
class Type_button:
    inline: str = "inline"
    reply: str = "reply"


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


async def add_new_button(text: str, type_button: str) -> None:
    """
    Добавляет новую кнопку с ручным управлением ID (увеличивает на 1 от максимального существующего)
    :param text: текст кнопки
    :param type_button: тип кнопки
    """
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
    """
    Получение списка пользователей с заданной ролью
    :param type_button:
    :return:
    """
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


"""PROGECTS"""



async def unpaid_bots_on_month(month: int, year: int):
    logging.info('unpaid_bots_on_month')
    async with async_session() as session:
        bots = await session.scalar(select(Progects)
            .where(Progects.paid_month < month)
            .where(Progects.paid_year < year)
            .where(Progects.state == state_bot.unpaid)
        )
        return bots

async def paid_bots_on_month(month: int, year: int):
    logging.info('paid_bots_on_month')
    async with async_session() as session:
        bots = await session.scalar(select(Progects)
            .where(Progects.paid_month >= month)
            .where(Progects.paid_year >= year)
            .where(Progects.state == state_bot.paid)
        )
        return bots

async def removed_bots():
    logging.info('paid_bots_on_month')
    async with async_session() as session:
        bots = await session.scalar(select(Progects)
            .where(Progects.state == state_bot.removed)
        )
        return bots