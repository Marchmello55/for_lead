from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from datetime import datetime
from aiogram.fsm.context import FSMContext


from database import requests as rq
from config_data.config import load_config, Config
from utils.texts import Message_for_user
from keyboards.server import inline_buttons as ib

import logging

router = Router()
config: Config = load_config()
text = Message_for_user()
now = datetime.now()

@router.callback_query(F.data == "server")
async def server_button(callback: CallbackQuery, bot: Bot):

    current_month_year = now.strftime("%M %Y")
    month, year=current_month_year.split(" ")
    if month!="10":month = int(month.replace("0", ""))
    await callback.message.answer("Выберите месяц для просмотра статуса ботов", reply_markup=await ib.built_inline_moth_and_pagination(month=int(month), year=int(year), prefix="server"))


@router.callback_query(F.data.startswith('server_year_'))
async def press_server_forward(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Пагинация по списку пользователей вперед
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_forward_del_admin: {callback.message.chat.id}')
    role = '<b>ИСПОЛНИТЕЛЕЙ</b>'
    list_users: list[User] = await rq.get_users_role(role=rq.UserRole.executor)
    forward = int(callback.data.split('_')[3]) + 1
    back = forward - 2
    keyboard = kb.keyboards_select_executor(list_executor=list_users,
                                            back=back,
                                            forward=forward,
                                            count=6)
    try:
        await callback.message.edit_text(text=f'Выберите пользователя, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.message.edit_text(text=f'Выберитe пользоватeля, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)


@router.callback_query(F.data.startswith('executor_back_'))
async def process_back_del_admin(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Пагинация по списку пользователей назад
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_back_del_admin: {callback.message.chat.id}')
    role = '<b>ИСПОЛНИТЕЛЕЙ</b>'
    list_users = await rq.get_users_role(role=rq.UserRole.executor)
    back = int(callback.data.split('_')[3]) - 1
    forward = back + 2
    keyboard = kb.keyboards_select_executor(list_executor=list_users,
                                            back=back,
                                            forward=forward,
                                            count=6)
    try:
        await callback.message.edit_text(text=f'Выберите пользователя, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.message.edit_text(text=f'Выберитe пользоватeля, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)


@router.callback_query(F.data.startswith('select_executor_'))
@error_handler
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