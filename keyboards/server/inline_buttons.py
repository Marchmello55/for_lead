from sys import prefix

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass


@dataclass
class Button_pagination:
    previous: str = "previous"
    next: str = "next"


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
        {"text": "Январь", "callback": f"{prefix}_choose_1.{year}"},{"text": "Февраль", "callback": f"{prefix}_choose_2.{year}"},{"text": "Март", f"callback": f"{prefix}_choose_3.{year}"},
        {"text": "Апрель", "callback": f"{prefix}_choose_4.{year}"},{"text": "Май", "callback": f"{prefix}_choose_5.{year}"},{"text": "Июнь", f"callback": f"{prefix}_choose_6.{year}"},
        {"text": "Июль", "callback": f"{prefix}_choose_7.{year}"},{"text": "Август", "callback": f"{prefix}_choose_8.{year}"},{"text": "Сентябрь", f"callback": f"{prefix}_choose_9.{year}"},
        {"text": "Октябрь", "callback": f"{prefix}_choose_10.{year}"},{"text": "Ноябрь", "callback": f"{prefix}_choose_11.{year}"},{"text": "Декабрь", f"callback": f"{prefix}_choose_12.{year}"}
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