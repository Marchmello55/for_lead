from datetime import datetime


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass

class ActionProjects:
    add_project = "add"
    info_project = "info"
    change_project = "change"
    task_project = "task"

class SectorProjects:
    ready_project = "ready"
    in_work_project = "in_work"
    canceled_project = "canceled"
    agrees_project = "agrees"
    all_project = "all"
    by_id_project = "by_id"
    by_name_project = "by_name"
    send_all_project = "send_all"



async def press_projects_buttons(prefix: str):
    buttons = []
    buttons.append({"text": "Добавить проект", "callback": f"{prefix}_{ActionProjects.add_project}"})
    buttons.append({"text": "Инфо о проектах", "callback": f"{prefix}_{ActionProjects.info_project}"})
    buttons.append({"text": "Изменить проект", "callback": f"{prefix}_{ActionProjects.change_project}"})
    buttons.append({"text": "Таски", "callback": f"{prefix}_{ActionProjects.task_project}"})
    return buttons