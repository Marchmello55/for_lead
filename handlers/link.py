from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command

from config_data.config import load_config, Config
from utils.texts import Message_for_user, Link

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()
text = Message_for_user()


@router.message(Command("link"))
async def process_press_help(message: Message, bot: Bot) -> None:
    link = Link(tg_id=message.from_user.id)
    user_id = message.from_user.id
    if user_id != int(config.tg_bot.support_id): return
    await message.answer(
        text=f'<a href="{link.link}">это ссылка</a>',
        parse_mode="HTML"
    )