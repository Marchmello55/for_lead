from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import calendar



# Кэш для хранения текущих дат пользователей
user_data = {}

async def generate_calendar_kb(prefix: str, year=None, month=None, highlight_day=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    highlight_day = highlight_day or now.day

    # Заголовок (год и месяц)
    month_name = datetime(year, month, 1).strftime("%b")
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    # Кнопки года и месяца
    kb.inline_keyboard.append([
        InlineKeyboardButton(text=f"<<", callback_data=f"{prefix}_back_year_{year}"),
        InlineKeyboardButton(text=f"[{year}]" if year == now.year else f"{year}", callback_data=f"none"),
        InlineKeyboardButton(text=f">>", callback_data=f"{prefix}_next_year_{year}")
    ])

    kb.inline_keyboard.append([
        InlineKeyboardButton(text=f"<", callback_data=f"{prefix}_back_month_{month}.{year}"),
        InlineKeyboardButton(text=f"[{calendar.month_name[month]}]" if month == now.month and year == now.year else f"{calendar.month_name[month]}", callback_data=f"none"),
        InlineKeyboardButton(text=f">", callback_data=f"{prefix}_next_month_{month}.{year}")
    ])

    kb.inline_keyboard.append([
        InlineKeyboardButton(text=" Mo ", callback_data="none"),
        InlineKeyboardButton(text=" Tu ", callback_data="none"),
        InlineKeyboardButton(text=" We ", callback_data="none"),
        InlineKeyboardButton(text=" Th ", callback_data="none"),
        InlineKeyboardButton(text=" Fr ", callback_data="none"),
        InlineKeyboardButton(text=" Sa ", callback_data="none"),
        InlineKeyboardButton(text=" Su ", callback_data="none"),
    ])

    # Генерация дней месяца
    month_cal = calendar.monthcalendar(year, month)
    for week in month_cal:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data=f"ignore"))
            else:
                text = f"[{day}]" if day == highlight_day and month == now.month and year == now.year else f" {day} "
                row.append(InlineKeyboardButton(text=text, callback_data=f"{prefix}_day_{day}.{month}.{year}"))
        kb.inline_keyboard.append(row)

    kb.inline_keyboard.append([
        InlineKeyboardButton(text="Cancel", callback_data=f"{prefix}_cancel"),
        InlineKeyboardButton(text="Today", callback_data=f"{prefix}_today")
    ])

    kb.inline_keyboard.append([
        InlineKeyboardButton(text="Главное меню", callback_data="main-menu")
    ])

    return kb

