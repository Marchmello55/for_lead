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


import logging


router = Router()
config: Config = load_config()
text = Message_for_user()
now = datetime.now()

class ProjectData(StatesGroup):
    bot_id = State()
    name = State()
    price = State()
    exercise = State()
    customer = State()
    link_to_chat = State()
    deadline = State()
    executor = State()

@router.callback_query(F.data == "projects")
@router.callback_query(F.data == "projects_back")
async def press_projects(callback: CallbackQuery, bot: Bot):
    action = ib.ActionProjects("project_action")
    await callback.message.edit_text(text="Взаимодействие с проектами", reply_markup=await bt.build_inline_keyboard(action.get_buttons()))
    await callback.answer()

@router.callback_query(F.data.startswith("project_action"))
async def press_project_action(callback: CallbackQuery, state: FSMContext, bot: Bot):
    action = callback.data.split("_")[2]
    sector = ib.SectorProjects("project_sector")
    for_state = ib.ForState("projects",[ib.ForState.back_button])#лучше заменить
    if action == ib.ActionProjects.add_project:
        await callback.message.edit_text(text="Проект (название или краткое описание)", reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
        await state.set_state(state=ProjectData.name)
    elif action == ib.ActionProjects.info_project:
        await callback.message.edit_text(text="Какие проекты вас интересуют?", reply_markup=await bt.build_inline_keyboard(sector.get_buttons_for_sector(ib.ActionProjects.info_project)))
    elif action == ib.ActionProjects.change_project:
        await callback.message.edit_text(text="Какие проекты вас интересуют?", reply_markup=await bt.build_inline_keyboard(sector.get_buttons_for_sector(ib.ActionProjects.change_project)))
    elif action == ib.ActionProjects.task_project:
        await callback.message.edit_text(text="Какие проекты вас интересуют?", reply_markup=await bt.build_inline_keyboard(sector.get_buttons_for_sector(ib.ActionProjects.task_project)))

"""@router.callback_query(F.data.startswith("project_sector"))
async def press_project_sector(callback: CallbackQuery, bot: Bot):"""
"""Работа с календарем"""


@router.callback_query(F.data.startwith("project_add-state_deadline"))
async def calendar_button(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Изменяем клавиатуру-календарь
    :param callback:
    :param state:
    :return:
    """
    logging.info("calendar_button")
    if "year" in callback.data:
        year = int(callback.data.split("year_")[1])
        if "next_year" in callback.data:
            prefix = callback.data.split("_next_year")[0]
            await callback.message.edit_reply_markup(await ic.generate_calendar_kb(prefix=prefix, year=year + 1))
        elif "back_year" in callback.data:
            prefix = callback.data.split("_back_year")[0]
            await callback.message.edit_reply_markup(await ic.generate_calendar_kb(prefix=prefix, year=year - 1))
    elif "month" in callback.data:
        month, year = str(callback.data.split("month_")[1]).split(".")
        if "next_month" in callback.data:
            prefix = callback.data.split("_next_month")[0]
            await callback.message.edit_reply_markup(await ic.generate_calendar_kb(prefix=prefix, year=year, month=int(month) + 1))
        elif "back_month" in callback.data:
            prefix = callback.data.split("_back_month")[0]
            await callback.message.edit_reply_markup(await ic.generate_calendar_kb(prefix=prefix, year=year, month=int(month) - 1))
    else:
        deadline = str(callback.data.split("day_")[1])
        bot_id: str = str(callback.data.split("_day")[0]).split("project_add-state_deadline_")[1]
        await rq.update_deadline(int(bot_id), deadline)
        #executors = await rq.
        #await callback.message.edit_text("Выберите человека на проект", reply_markup=await bt.build_inline_keyboard_and_pagination())
    await callback.answer()


"""Добавить проекты"""

@router.message(F.text, StateFilter(ProjectData.name))
async def get_project_name(message: Message, state: FSMContext) -> None:
    """
    Получаем полное название или краткое описание
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_name')
    name = str(message.text)
    await rq.add_bot(name)
    bot_id = await rq.get_bot_id_by_name(name)
    await state.update_data(bot_id=bot_id.bot_id)
    for_state = ib.ForState(f"project_add-state_price_{bot_id.bot_id}",[ib.ForState.skip_button, ib.ForState.main_menu_button])
    await message.answer(text='Стоимость проекта', reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
    await state.set_state(state=ProjectData.price)


@router.message(F.text, StateFilter(ProjectData.price))
async def get_project_price(message: Message, state: FSMContext) -> None:
    """
    Получаем цену проекта
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_price')
    price = str(message.text)
    bot_id = int(dict(await state.get_data())["bot_id"])
    for_state = ib.ForState(f"project_add-state_exercise_{bot_id}", [ib.ForState.skip_button, ib.ForState.main_menu_button])
    await rq.update_price(bot_id, price)
    await message.answer(text='Добавьте описание ТЗ', reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
    await state.set_state(state=ProjectData.exercise)

@router.message(F.text, StateFilter(ProjectData.exercise))
async def get_project_exercise(message: Message, state: FSMContext) -> None:
    """
    Получаем тз
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_exercise')
    exercise = str(message.text)
    bot_id = int(dict(await state.get_data())["bot_id"])
    for_state = ib.ForState(f"project_add-state_customer_{bot_id}", [ib.ForState.main_menu_button])
    await rq.add_bot(exercise)
    await message.answer(text='Добавьте контакт заказчика (username or link)', reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
    await state.set_state(state=ProjectData.customer)


@router.message(F.text, StateFilter(ProjectData.customer))
async def get_project_customer(message: Message, state: FSMContext) -> None:
    """
    Получаем контакт заказчика
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_customer')
    customer = str(message.text)
    bot_id = int(dict(await state.get_data())["bot_id"])
    for_state = ib.ForState(f"project_add-state_link-to-chat_{bot_id}", [ib.ForState.skip_button, ib.ForState.main_menu_button])
    await rq.add_bot(customer)
    await message.answer(text='Добавьте ссылку на обсуждение проекта', reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
    await state.set_state(state=ProjectData.link_to_chat)


@router.message(F.text, StateFilter(ProjectData.link_to_chat))
async def get_project_link_to_chat(message: Message, state: FSMContext) -> None:
    """
    Получаем ссылку на чат с обсуждением проекта
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_link_to_chat')
    link_to_chat = str(message.text)
    bot_id = int(dict(await state.get_data())["bot_id"])
    await rq.add_bot(link_to_chat)
    await message.answer(text='Когда должно быть готово?', reply_markup=await ic.generate_calendar_kb(f"project_add-state_deadline_{bot_id}"))



@router.message(F.text, StateFilter(ProjectData.deadline))
async def get_project_exercise(message: Message, state: FSMContext) -> None:
    """
    Получаем
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_exercise')
    name = str(message.text)
    for_state = ib.ForState("project_add-state", [ib.ForState.main_menu_button])
    await rq.add_bot(name)
    await message.answer(text='Выиберите человека на проект', reply_markup=await bt.build_inline_keyboard_and_pagination())
    await state.set_state(state=ProjectData.customer)


@router.message(F.text, StateFilter(ProjectData.executor))
async def get_project_exercise(message: Message, state: FSMContext) -> None:
    """
    Получаем тз
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_project_exercise')
    name = str(message.text)
    for_state = ib.ForState("project_add-state", [ib.ForState.main_menu_button])
    await rq.add_bot(name)
    await message.answer(text='Заказчик (username or link)', reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
    await state.set_state(state=ProjectData.customer)

