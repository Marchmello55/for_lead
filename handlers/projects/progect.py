from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter


from config_data.config import load_config, Config
from keyboards.progects import inline_buttons as ib
from keyboards import buttons as bt
from keyboards import inline_calendar as ic

import logging

router = Router()
config: Config = load_config()

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
    logging.info("press_projects")
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


@router.callback_query(F.data.startswith("project_add-state") & F.data.endswith("_skip"))
async def skip_buttons(callback: CallbackQuery, state: FSMContext):
    logging.info("skip_buttons")
    await callback.answer()
    bot_id = int(dict(await state.get_data())["bot_id"])
    add_state = str(callback.data.split("_")[2])
    if add_state == "price":
        for_state = ib.ForState(f"project_add-state_exercise_{bot_id}", [ib.ForState.skip_button, ib.ForState.main_menu_button])
        await callback.message.answer(text='Добавьте описание ТЗ',reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
        await state.set_state(state=ProjectData.exercise)
    elif add_state == "exercise":
        bot_id = int(dict(await state.get_data())["bot_id"])
        for_state = ib.ForState(f"project_add-state_customer_{bot_id}", [ib.ForState.main_menu_button])
        await callback.message.answer(text='Добавьте контакт заказчика (username or link)', reply_markup=await bt.build_inline_keyboard(for_state.get_buttons()))
        await state.set_state(state=ProjectData.customer)
    elif add_state == "link-to-chat":
        bot_id = int(dict(await state.get_data())["bot_id"])
        await callback.message.answer(text='Когда должно быть готово?', reply_markup=await ic.generate_calendar_kb(f"project_add-state_deadline_{bot_id}"))