from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext
from sqlalchemy.util import await_fallback

from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards.server import inline_buttons as ib


import logging


router = Router()
config: Config = load_config()
text = Message_for_user()
now = datetime.now()

month_names = {
    "1": "январь",
    "2": "февраль",
    "3": "март",
    "4": "апрель",
    "5": "май",
    "6": "июнь",
    "7": "июль",
    "8": "август",
    "9": "сентябрь",
    "10": "октябрь",
    "11": "ноябрь",
    "12": "декабрь"
}

@router.callback_query(F.data == "server")
async def server_button(callback: CallbackQuery, bot: Bot):

    current_month_year = now.strftime("%m %Y")
    month, year=current_month_year.split(" ")
    if month!="10":month = int(month.replace("0", ""))
    if not await rq.get_unpaid_bots_on_month(month=int(month), year=int(year)):
        await callback.message.answer("Выберите месяц для просмотра статуса ботов", reply_markup=await ib.built_inline_moth_and_pagination(month=int(month), year=int(year), prefix="server"))
    else:
        bots = await rq.get_unpaid_bots_on_month(month=int(month), year=int(year))
        await callback.message.edit_text(f"Выберите месяц для просмотра статуса ботов\n\n!!! у вас {len(bots)} не оплаченных ботов!!!", reply_markup=await ib.built_inline_moth_and_pagination(month=int(month), year=int(year), prefix="server"))
    await callback.answer()

@router.callback_query(F.data.startswith('server_year_'))
async def press_server(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Пагинация по списку пользователей вперед
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'press_server_forward')
    if callback.data.split('_')[3] == ib.Button_pagination.previous:
        year = int(callback.data.split('_')[2]) - 1
    else:
        year = int(callback.data.split('_')[2]) + 1
    await callback.message.edit_text("Выберите месяц для просмотра статуса ботов", reply_markup=await ib.built_inline_moth_and_pagination(year=int(year), prefix="server"))
    await callback.answer()

@router.callback_query(F.data.startswith('server_choose'))
async def press_server_choose_month(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info("press_server_choose_month")
    month, year = callback.data.split('_')[2].split('.')
    buttons = []
    states = ib.ServerState(prefix=f"server_state", month=month, year=year)
    if await rq.get_unpaid_bots_on_month(month=int(month), year=int(year)): buttons.append(states.unpaid)
    if await rq.get_paid_bots_on_month(month=int(month), year=int(year)): buttons.append(states.paid)
    if await rq.get_removed_bots_on_month(month=int(month), year=int(year)): buttons.append(states.removed)
    if len(buttons) !=0:await callback.message.answer(f"Боты на {month_names[f"{int(month)}"]}", reply_markup=await ib.build_inline_keyboard(buttons))
    else: await callback.message.answer("Ботов нет")
    await callback.answer()

#это надо фиксить

@router.callback_query(F.data.startswith(f'server_{ib.ServerState.state_paid}',f'server_{ib.ServerState.state_unpaid}',f'server_{ib.ServerState.state_remove}'))
async def press_server_choose_state(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info("press_server_choose_state")
    state = callback.data.split('_')[3]
    month, year = callback.data.split('_')[4].split('.')
    if state == ib.ServerState.state_paid:
        bots: list = await rq.get_paid_bots_on_month(month=int(month), year=int(year))
        await callback.message.answer(f"Оплаченные боты на {month_names[int(month)]}", reply_markup=await ib.build_inline_keyboard_and_pagination(prefix=f"server_bot_paid_{month}.{year}", list_users=bots))
    elif state == ib.ServerState.state_unpaid:
        bots: list = await rq.get_paid_bots_on_month(month=int(month), year=int(year))
        await callback.message.answer(f"Неоплаченные боты на {month_names[int(month)]}", reply_markup=await ib.build_inline_keyboard_and_pagination(prefix=f"server_bot_unpaid_{month}.{year}", list_users=bots))
    elif state == ib.ServerState.state_remove:
        bots: list = await rq.get_paid_bots_on_month(month=int(month), year=int(year))
        await callback.message.answer(f"Снятые с работы боты на {month_names[int(month)]}", reply_markup=await ib.build_inline_keyboard_and_pagination(prefix=f"server_bot_remove_{month}.{year}", list_users=bots))
    await callback.answer()

@router.callback_query(F.data.startswith('sheet_server_bot'))
async def press_choose_sheet(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info("press_server_choose_sheet")
    num_sheet = int(callback.data.split("_")[-1])
    month, year = str(callback.data.split("_")[4]).split(".")
    state = callback.data.split("_")[3]
    if state == ib.ServerState.state_paid: bots: list = await rq.get_paid_bots_on_month(month=int(month), year=int(year))
    elif state == ib.ServerState.state_unpaid: bots: list = await rq.get_unpaid_bots_on_month(month=int(month), year=int(year))
    elif state == ib.ServerState.state_remove: bots: list = await rq.get_removed_bots_on_month(month=int(month), year=int(year))
    await callback.message.edit_reply_markup(reply_markup=await ib.build_inline_keyboard_and_pagination(prefix=f"server_bot_{state}_{month}.{year}", list_users=bots, sheet=num_sheet))
    await callback.answer()
    
@router.callback_query(F.data.startswith('select_server_bot'))
async def press_select_bot(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info("press_server_select_bot")
    month, year = str(callback.data.split("_")[4]).split(".")
    state = callback.data.split("_")[3]
    bot_id = int(callback.data.split("_")[-1])

