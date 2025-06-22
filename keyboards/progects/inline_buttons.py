from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InlineButton:
    def __init__(self, text: str, prefix: str, action: str):
        self.data = {
            "text": text,
            "callback": f"{prefix}_{action}"
        }


class BaseActions:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.buttons = []

    def _add_button(self, text: str, action: str):
        self.buttons.append({
            "text": text,
            "callback": f"{self.prefix}_{action}"
        })

    def _add_button_no_prefix(self, text: str, action: str):
        self.buttons.append({"text": text,
            "callback": f"{action}"})

    def get_buttons(self):
        return self.buttons


class ActionProjects(BaseActions):
    add_project = "add"
    info_project = "info"
    change_project = "change"
    task_project = "task"

    def __init__(self, prefix: str):
        super().__init__(prefix)
        self._add_button("Добавить проект", self.add_project)
        self._add_button("Инфо о проектах", self.info_project)
        self._add_button("Изменить проект", self.change_project)
        self._add_button("Таски", self.task_project)


class SectorProjects(BaseActions):
    ready_project = "ready"
    in_work_project = "in_work"
    canceled_project = "canceled"
    agrees_project = "agrees"
    all_project = "all"
    by_id_project = "by_id"
    by_name_project = "by_name"
    send_all_project = "send_all"

    def __init__(self, prefix: str):
        super().__init__(prefix)
        self._add_button("✅ Готовые", self.ready_project)
        self._add_button("🛠 В работе", self.in_work_project)
        self._add_button("❌ Отмененные", self.canceled_project)
        self._add_button("🕑 На согласовании", self.agrees_project)
        self._add_button("Все проекты", self.all_project)
        self._add_button("Поиск по ID", self.by_id_project)
        self._add_button("Поиск по названию", self.by_name_project)
        self._add_button("Все проекты сообщением", self.send_all_project)

    def get_buttons_for_sector(self, sector: str):
        if sector == ActionProjects.info_project:
            return self.buttons
        elif sector == ActionProjects.change_project:
            return [btn for btn in self.buttons if btn["callback"] != f"{self.prefix}_{self.send_all_project}"]
        elif sector == ActionProjects.task_project:
            return [btn for btn in self.buttons if btn["callback"] not in [
                f"{self.prefix}_{self.canceled_project}",
                f"{self.prefix}_{self.agrees_project}",
                f"{self.prefix}_{self.send_all_project}"
            ]]


class ForState(BaseActions):
    back_button = "back"
    skip_button = "skip"
    main_menu_button = "main-menu"

    def __init__(self, prefix: str, need_buttons: list):
        super().__init__(prefix)
        if self.skip_button in need_buttons: self._add_button("Пропустить", self.skip_button)
        if self.back_button in need_buttons: self._add_button("Назад", self.back_button)
        if self.main_menu_button in need_buttons: self._add_button_no_prefix("Главное меню", self.main_menu_button)