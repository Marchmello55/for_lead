from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass


@dataclass
class Button_pagination:
    previous: str = "previous"
    next: str = "next"


async def built_inline_moth_and_pagination(year: int, prefix: str, month = None):
    data = [
        {"text": "Январь", "callback": f"{prefix}_01.{year}"},{"text": "Февраль", "callback": f"{prefix}_02.{year}"},{"text": "Март", f"callback": f"{prefix}_03.{year}"},
        {"text": "Апрель", "callback": f"{prefix}_04.{year}"},{"text": "Май", "callback": f"{prefix}_05.{year}"},{"text": "Июнь", f"callback": f"{prefix}_06.{year}"},
        {"text": "Июль", "callback": f"{prefix}_07.{year}"},{"text": "Август", "callback": f"{prefix}_08.{year}"},{"text": "Сентябрь", f"callback": f"{prefix}_09.{year}"},
        {"text": "Октябрь", "callback": f"{prefix}_10.{year}"},{"text": "Ноябрь", "callback": f"{prefix}_11.{year}"},{"text": "Декабрь", f"callback": f"{prefix}_12.{year}"}
    ]
    builder = InlineKeyboardBuilder()

    if month:
        for button in data[month-1:]:
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
    builder.button(
        text="⬅️",
        callback_data=f"{prefix}_year_{year}_{Button_pagination.previous}"
    )
    builder.button(
        text=f"{year}",
        callback_data=""
    )
    builder.button(
        text="➡️",
        callback_data=f"{prefix}_year_{year}_{Button_pagination.next}"
    )
    builder.adjust(3)
    return builder.as_markup()