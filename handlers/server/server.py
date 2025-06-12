from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext


from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards.server import inline_buttons as ib
from keyboards import buttons as bt

import logging


router = Router()
config: Config = load_config()
text = Message_for_user()
now = datetime.now()

month_names = {
    1: "январь",
    2: "февраль",
    3: "март",
    4: "апрель",
    5: "май",
    6: "июнь",
    7: "июль",
    8: "август",
    9: "сентябрь",
    10: "октябрь",
    11: "ноябрь",
    12: "декабрь"
}

@router.callback_query(F.data == "server")
async def server_button(callback: CallbackQuery, bot: Bot):

    current_month_year = now.strftime("%M %Y")
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
    if callback.data.split('_')[2] == ib.Button_pagination.previous:
        year = int(callback.data.split('_')[3]) - 1
    else:
        year = int(callback.data.split('_')[3]) + 1
    await callback.message.edit_text("Выберите месяц для просмотра статуса ботов", reply_markup=await ib.built_inline_moth_and_pagination(year=int(year), prefix="server"))
    await callback.answer()

@router.callback_query(F.data.startswith('server_choose'))
async def press_server_choose_month(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info("press_server_choose_month")
    month, year = callback.data.split('_')[3].split('.')
    buttons = []
    states = ib.ServerState(prefix=f"server_state", month=month, year=year)
    if await rq.get_unpaid_bots_on_month(month=int(month), year=int(year)): buttons.append(states.unpaid)
    if await rq.get_paid_bots_on_month(month=int(month), year=int(year)): buttons.append(states.paid)
    if await rq.get_removed_bots_on_month(month=int(month), year=int(year)): buttons.append(states.removed)
    if len(buttons) !=0:await callback.message.answer(f"Боты на {month_names[int(month)]}", reply_markup=await bt.build_inline_keyboard(buttons))
    else: await callback.message.answer("Ботов нет")
    await callback.answer()

@router.callback_query(F.data.startswith('server_state'))
async def press_server_choose_state(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info("press_server_choose_state")
    state = callback.data.split('_')[3]
    month, year = callback.data.split('_')[4].split('.')
    if state == ib.ServerState.state_paid:
        bots = await rq.get_paid_bots_on_month(month=int(month), year=int(year))
        await callback.message.answer(f"Оплаченные боты на {month_names[int(month)]}", reply_markup=await bt.build_inline_keyboard_and_pagination(prefix="server_bot", list_users=bots))


@router.callback_query(F.data.startswith('select_executor_'))
async def process_select_executor(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Назначение исполнителя на заявку
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_select_executor: {callback.message.chat.id}')
    data = await state.get_data()
    tg_id_executor = int(callback.data.split('_')[-1])
    order_id = data['order_id']
    info_order: Order = await rq.get_order_id(order_id=int(order_id))
    info_executor: User = await rq.get_user_by_id(tg_id=tg_id_executor)
    if not info_order.photo_ids:
        await bot.send_message(chat_id=tg_id_executor,
                               text=info_order.text_order,
                               reply_markup=None)
    else:
        media_group = []
        i = 0
        for photo in info_order.photo_ids.split(','):
            i += 1
            if i == 1:
                media_group.append(InputMediaPhoto(media=photo, caption=info_order.text_order))
            else:
                media_group.append(InputMediaPhoto(media=photo))
        await bot.send_media_group(chat_id=tg_id_executor,
                                   media=media_group)
    await bot.send_message(chat_id=tg_id_executor,
                           text=f'Вы назначены <b>ИСПОЛНИТЕЛЕМ</b> в для решения заявки № {order_id}'
                                f' - {info_order.type_order}.'
                                f'После решения отправьте отчет выбрав номер обращения в разделе "ЗАЯВКИ"',
                           reply_markup=None)
    await callback.message.edit_text(text=f'Пользователь'
                                          f' <a href="tg://user?id={tg_id_executor}">{info_executor.username}</a> '
                                          f'назначен для выполнения заявки № {order_id} - {info_order.type_order}.\n'
                                          f'Статус заявки поступит вам при ее изменении, а также вы можете просмотреть'
                                          f' все опубликованные заявки в разделе "ЗАЯВКИ"')
    await bot.send_message(chat_id=info_order.tg_id,
                           text=f'Пользователь'
                                f' <a href="tg://user?id={tg_id_executor}">{info_executor.username}</a> '
                                f'назначен для выполнения заявки № {order_id} - {info_order.type_order}.\n'
                                f'Статус заявки поступит вам при ее изменении')
    await rq.set_order_status(order_id=int(order_id),
                              status=rq.OrderStatus.work)
    await rq.set_order_executor(order_id=int(order_id),
                                executor=tg_id_executor)
    await callback.answer()