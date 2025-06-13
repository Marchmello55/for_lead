from datetime import datetime


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass


@dataclass
class Button_pagination:
    previous: str = "previous"
    next: str = "next"

now = datetime.now()


class ServerState:
    state_paid: str = "paid"
    state_unpaid: str = "unpaid"
    state_remove: str = "remove"
    def __init__(self, prefix: str, month: str, year: str):
        self.paid = {
            "text": "✅ Оплаченные",
            "callback": f"{prefix}_{self.state_paid}_{month}.{year}"
        }
        self.unpaid = {
            "text": "❌ Не оплаченные",
            "callback": f"{prefix}_{self.state_unpaid}_{month}.{year}"
        }
        self.removed = {
            "text": "🟡 Снятые с работы",
            "callback": f"{prefix}_{self.state_remove}_{month}.{year}"
        }


async def built_inline_moth_and_pagination(year: int, prefix: str, month = None):
    data = [
        {"text": "Январь", "callback": f"{prefix}_choose_1.{year}"},{"text": "Февраль", "callback": f"{prefix}_choose_2.{year}"},{"text": "Март", "callback": f"{prefix}_choose_3.{year}"},
        {"text": "Апрель", "callback": f"{prefix}_choose_4.{year}"},{"text": "Май", "callback": f"{prefix}_choose_5.{year}"},{"text": "Июнь", "callback": f"{prefix}_choose_6.{year}"},
        {"text": "Июль", "callback": f"{prefix}_choose_7.{year}"},{"text": "Август", "callback": f"{prefix}_choose_8.{year}"},{"text": "Сентябрь", "callback": f"{prefix}_choose_9.{year}"},
        {"text": "Октябрь", "callback": f"{prefix}_choose_10.{year}"},{"text": "Ноябрь", "callback": f"{prefix}_choose_11.{year}"},{"text": "Декабрь", "callback": f"{prefix}_choose_12.{year}"}
    ]
    builder = InlineKeyboardBuilder()
    current_year = int(now.strftime("%Y"))
    if month or year == current_year:
        if not month: month = int(now.strftime("%m"))
        for button in data[int(month)-1:]:
            builder.button(
                text=button["text"],
                callback_data=button["callback"]
            )
    else:
        for button in data:
            builder.button(
                text=button["text"],
                callback_data=button["callback"]
            )
    if month:
        if len(data[int(month)])%3!=0:
            for i in range(len(data[int(month)-1])%3):
                builder.button(
                    text=" ",
                    callback_data=f"none"
                )
    builder.button(
        text="⬅️",
        callback_data=f"{prefix}_year_{year}_{Button_pagination.previous}"
    )
    builder.button(
        text=f"{year}",
        callback_data="none"
    )
    builder.button(
        text="➡️",
        callback_data=f"{prefix}_year_{year}_{Button_pagination.next}"
    )
    builder.adjust(3)
    return builder.as_markup()

async def build_inline_keyboard(data: list[dict]) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру на основе кнопок из БД
    :param data: список словарей с данными кнопок
    :return: объект InlineKeyboardMarkup
    """
    """
    data = [
        {"text": "...", "callback": "..."},
        {"text": "...", "callback": "..."}
    ]
    """
    builder = InlineKeyboardBuilder()

    for button in data:
        builder.button(
            text=button["text"],
            callback_data=button["callback"]
        )

    builder.adjust(1)

    return builder.as_markup()

async def button_for_list_bots_and_pagination(list_bots: list, prefix: str, sheet: int = 0, count:int = 6) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру на основе кнопок из БД
    :param data: список словарей с данными кнопок
    :return: объект InlineKeyboardMarkup
    """
    date = prefix.split("_")[-1]
    main_prefix = prefix.split("_")[0]
    forward = sheet + 1
    back = sheet - 1
    # считаем сколько всего блоков по заданному количество элементов в блоке
    count_users = len(list_bots)
    whole = count_users // count
    remains = count_users % count
    max_forward = whole + 1
    # если есть остаток, то увеличиваем количество блоков на один, чтобы показать остаток
    if remains:
        max_forward = whole + 2
    if forward >= max_forward:
        forward = max_forward
        back = forward - 2
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for bot in list_bots[back*count:(forward-1)*count]:
        text = bot.name
        button = f'select_{prefix}_{bot.id}'
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    if back >= 0:
        button_back = InlineKeyboardButton(text='⬅️',
                                           callback_data=f'sheet_{prefix}_{str(back)}')
    else:
        button_back = InlineKeyboardButton(text=' ',
                                           callback_data=f'none')
    button_count = InlineKeyboardButton(text=f'{sheet+1}',
                                        callback_data='none')
    button_next = InlineKeyboardButton(text='➡️',
                                       callback_data=f'sheet_{main_prefix}_{str(forward)}')

    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_count, button_next)

    return kb_builder.as_markup()

# шаблон

async def build_inline_keyboard_and_pagination(list_users: list, prefix: str, sheet: int=0, count:int = 6) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру на основе кнопок из БД
    :param data: список словарей с данными кнопок
    :return: объект InlineKeyboardMarkup
    """
    date = prefix.split("_")[-1]
    main_prefix = prefix.split("_")[0]
    forward = sheet + 1
    back = sheet - 1
    # считаем сколько всего блоков по заданному количество элементов в блоке
    count_users = len(list_users)
    whole = count_users // count
    remains = count_users % count
    max_forward = whole + 1
    # если есть остаток, то увеличиваем количество блоков на один, чтобы показать остаток
    if remains:
        max_forward = whole + 2
    if forward >= max_forward:
        forward = max_forward
        back = forward - 2
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for bot in list_users[back*count:(forward-1)*count]:
        text = bot.name
        button = f'{prefix}_select_{bot.id}'
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    if back >= 0:
        button_back = InlineKeyboardButton(text='⬅️',
                                           callback_data=f'{prefix}_sheet_{str(back)}')
    else:
        button_back = InlineKeyboardButton(text=' ',
                                           callback_data=f'none')
    button_count = InlineKeyboardButton(text=f'{sheet+1}',
                                        callback_data='none')
    button_next = InlineKeyboardButton(text='➡️',
                                       callback_data=f'{main_prefix}_sheet_{str(forward)}')

    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_count, button_next)

    return kb_builder.as_markup()