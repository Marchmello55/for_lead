from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext
from sqlalchemy.util import await_fallback
from aiogram.fsm.state import State, StatesGroup


from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards.progects import inline_buttons as ib
from keyboards import buttons as bt


import logging


router = Router()
config: Config = load_config()
text = Message_for_user()
now = datetime.now()

class ProjectData(StatesGroup):
    name = State()
    price = State()
    exercise = State()
    customer = State()
    link_to_chat = State()
    deadline = State()
    executor = State()

@router.callback_query(F.data == "projects")
async def press_projects(callback: CallbackQuery, bot: Bot):
    action = ib.ActionProjects("project_action")
    await callback.message.answer(text="Взаимодействие с проектами", reply_markup=await bt.build_inline_keyboard(action.get_buttons()))
    await callback.answer()

@router.callback_query(F.data.startswith("project_action"))
async def press_project_action(callback: CallbackQuery, bot: Bot):
    action = callback.data.split("_")[2]
    sector = ib.SectorProjects("project_sector")
    for_state = ib.ForState("project_add-state")
    if action == ib.ActionProjects.add_project:
        await callback.message.edit_text(text="Проект (название или краткое описание", reply_markup= )
    elif action == ib.ActionProjects.info_project:
        await callback.message.edit_text(text="Какие проекты вас интересуют?", reply_markup=await bt.build_inline_keyboard(sector.get_buttons_for_sector(ib.ActionProjects.info_project)))
    elif action == ib.ActionProjects.change_project:
        await callback.message.edit_text(text="Какие проекты вас интересуют?", reply_markup=await bt.build_inline_keyboard(sector.get_buttons_for_sector(ib.ActionProjects.change_project)))
    elif action == ib.ActionProjects.task_project:
        await callback.message.edit_text(text="Какие проекты вас интересуют?", reply_markup=await bt.build_inline_keyboard(sector.get_buttons_for_sector(ib.ActionProjects.task_project)))

@router.callback_query(F.data.startswith("project_sector"))
async def press_project_sector(callback: CallbackQuery, bot: Bot):
