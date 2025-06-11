import asyncio
import datetime

from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto, ChatInviteLink
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter, CommandObject

from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user, Sum
from keyboards import buttons as bt

import logging

router = Router()
config: Config = load_config()
text = Message_for_user()


@router.message(Command("add"))
async def add_handler(message: Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id != int(config.tg_bot.support_id):
        return

    if not command.args:
        await message.answer("Ошибка: Укажите число (например /add 10.5)")
        return

    try:
        num_str = command.args.replace(',', '.')  # Для поддержки запятых
        if not num_str.replace('.', '', 1).isdigit():
            raise ValueError

        sum_obj = Sum(quantity=float(num_str))
        await rq.add_new_button(
            text=sum_obj.formatted_sum,  # "10.50 RUB"
            type_button="inline"
        )
        await message.answer(f"Добавлено: {sum_obj.formatted_sum}")

    except ValueError:
        await message.answer("Ошибка: Введите корректное число (например 15 или 7.5)")