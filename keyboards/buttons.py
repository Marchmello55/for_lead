from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass


@dataclass
class text_button:
    user: str = "user"
    user: str = "user"
    user: str = "user"


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

async def build_inline_keyboard_and_pagination(list_users: list, back, forward, count, prefix: str) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру на основе кнопок из БД
    :param data: список словарей с данными кнопок
    :return: объект InlineKeyboardMarkup
    """
    if back < 0:
        back = 0
        forward = 2
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
    print(back, forward, max_forward)
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for user in list_users[back*count:(forward-1)*count]:
        text = user.username
        button = f'{prefix}{user.tg_id}'
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    button_back = InlineKeyboardButton(text='<<<<',
                                       callback_data=f'{prefix}_{str(back)}')
    button_count = InlineKeyboardButton(text=f'{back+1}',
                                        callback_data='none')
    button_next = InlineKeyboardButton(text='>>>>',
                                       callback_data=f'{prefix}_{str(forward)}')

    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_count, button_next)

    return kb_builder.as_markup()
