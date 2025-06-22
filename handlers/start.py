from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards import buttons as bt
from keyboards.progects import inline_buttons as ib

import logging

router = Router()
config: Config = load_config()
text = Message_for_user()


@router.message(CommandStart())
async def process_press_start(message: Message, bot: Bot):
    if message.from_user.id == int(config.tg_bot.support_id):
        data = [
            {"text": "Подчиненные", "callback": "subordinates"},
            {"text": "Проекты", "callback": "projects"},
            {"text": "Сервер", "callback": "server"}
        ]
        name = message.from_user.username or message.from_user.first_name
        await message.answer(f'Доброго времени суток, {name}',reply_markup=await bt.build_inline_keyboard(data))

@router.callback_query(F.data == "main-menu")
async def process_main_menu_callback(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id == int(config.tg_bot.support_id):
        data = [
            {"text": "Подчиненные", "callback": "subordinates"},
            {"text": "Проекты", "callback": "projects"},
            {"text": "Сервер", "callback": "server"}
        ]
        name = callback.from_user.username or callback.from_user.first_name
        await callback.message.edit_text(
            f'Доброго времени суток, {name}',
            reply_markup=await bt.build_inline_keyboard(data)
        )
    await callback.answer()