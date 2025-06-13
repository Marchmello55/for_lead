from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart

from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards import buttons as bt

import logging

router = Router()
config: Config = load_config()
text = Message_for_user()

@router.message(CommandStart())
async def process_press_start(message: Message, bot: Bot):
    if message.from_user.id == int(config.tg_bot.support_id):
        data = [
            {"text": "Подчиненные", "callback": "subordinates"},
            {"text": "Проекты", "callback": "progects"},
            {"text": "Сервер", "callback": "server"}
        ]
        name = message.from_user.username or message.from_user.first_name
        await message.answer(f'Доброго времени суток, {name}',reply_markup=await bt.build_inline_keyboard(data))