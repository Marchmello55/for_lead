from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext
from sqlalchemy.util import await_fallback
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter


from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards.progects import inline_buttons as ib
from keyboards import buttons as bt
from keyboards import inline_calendar as ic
from handlers.projects.progect import ProjectData

import logging

router = Router()
config: Config = load_config()
text = Message_for_user()
now = datetime.now()

class ParseData(StatesGroup):
    bot_id = State()
    name = State()

line_text = "______________________________________________________________________"

async def create_text_for_projects(data):
    text = f"""id: {data.bot_id}\n
                {data.name} - {data.price if data.price != "" else "Цена не указана"}\n
                {data.exercise if data.exercise != "" else "ТЗ не указано"}\n
                {data.customer}\n 
                {data.link_to_chat if data.link_to_chat != "" else "Ссылки на обсуждение проекта нет"}\n
                {data.executor if data.executor != "" else "Исполитель не назначен"}\n
                {data.deadline}\n
                {data.report if data.customer != "" else "Отчетов нет"}\n
                """
    return text



@router.callback_query(F.data.startswith("project_sector"))
async def press_project_sector(callback: CallbackQuery, state: FSMContext):
    logging.info("press_project_sector")
    sector = callback.data.split("_")[2]
    await callback.answer()
    if sector == "ready":
        bots = await rq.get_ready_projects()
        if not bots:
            await callback.message.answer("Нет подходящих проектов")
            return
        await callback.message.answer(text=await create_text_for_projects(bots[0]),
                                      reply_markup=await ib.buttons_for_projects(bot_data_id=0,prefix="project", data=bots))
    elif sector == "in-work":
        bots = await rq.get_in_work_projects()
        if not bots:
            await callback.message.answer("Нет подходящих проектов")
            return 
        await callback.message.answer(text=await create_text_for_projects(bots[0]),
                                      reply_markup=await ib.buttons_for_projects(bot_data_id=0,prefix="project", data=bots))
    elif sector == "canceled":
        bots = await rq.get_canceled_projects()
        if not bots:
            await callback.message.answer("Нет подходящих проектов")
            return
        await callback.message.answer(text=await create_text_for_projects(bots[0]),
                                      reply_markup=await ib.buttons_for_projects(bot_data_id=0,prefix="project", data=bots))
    elif sector == "agrees":
        bots = await rq.get_agrees_projects()
        if not bots:
            await callback.message.answer("Нет подходящих проектов")
            return
        await callback.message.answer(text=await create_text_for_projects(bots[0]),
                                      reply_markup=await ib.buttons_for_projects(bot_data_id=0,prefix="project", data=bots))
    elif sector == "all":
        bots = await rq.get_all_projects()
        if not bots:
            await callback.message.answer("Нет подходящих проектов")
            return
        await callback.message.answer(text=await create_text_for_projects(bots[0]),
                                      reply_markup=await ib.buttons_for_projects(bot_data_id=0,prefix="project", data=bots))
    elif sector == "by_id":
        await callback.message.answer("Введите id проекта")
        await state.set_state(state=ParseData.bot_id)
    elif sector == "by_name":
        await callback.message.answer("Введите id проекта")
        await state.set_state(state=ParseData.name)
    elif sector == "send_all":
        text_to_message = []
        text_to_element_list = ""
        bots = await rq.get_all_projects()
        for bot in bots:
            bot_text = await create_text_for_projects(bot)
            if len(text_to_element_list) + len(bot_text) > 4025:
                text_to_message.append(text_to_element_list + "\n" + line_text)
                text_to_element_list = bot_text + "\n" + line_text + "\n"
            elif len(bot_text)>=4096 and text_to_element_list == "":
                text_to_message.append(bot_text)
            elif len(bot_text)>=4096 and text_to_element_list != "":
                text_to_message.append(text_to_element_list)
                text_to_message.append(bot_text)
            else: await callback.message.answer("есть недоработка в создании сообщения")


@router.message(F.text, StateFilter(ParseData.bot_id))
async def get_parse_data_bot_id(message: Message) -> None:
    logging.info(f'get_parse_data_bot_id')
    if not message.text.isdigit():
        await message.answer("Вы указали id не в том формате (укажите цыфрами id)")
        return
    bot_id = int(message.text)
    if bot_id != await rq.get_bot_id(bot_id):
        await message.answer("Вы указали id, которого нет, попробуйте еще раз")
        return
    await message.answer(text=await create_text_for_projects(await rq.get_bot_id(bot_id)))

@router.message(F.text, StateFilter(ParseData.name))
async def get_parse_data_name(message: Message) -> None:
    logging.info(f'get_parse_data_name')
    await message.answer("а как?")