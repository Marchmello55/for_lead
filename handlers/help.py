import asyncio
import datetime

from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command


from config_data.config import load_config, Config
from utils.texts import Message_for_user

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()
text = Message_for_user()

@router.message(Command("help"))
async def process_press_help(message: Message) -> None:
    #logging.log('process_press_help')
    if message.from_user.id == int(config.tg_bot.support_id):await message.answer(text=text.help_message_admin)
    else: await message.answer(text=text.help_message)