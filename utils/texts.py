from dataclasses import  dataclass


@dataclass
class Message_for_user:
    first_hello_message: str = ("Привет, я бот котороый поможет тебе,"
                                "\nнапиши /help для сипска комманд с инструкцией использования")
    help_message_admin: str = ("- /start → Приветственное сообщение.\n"
                         "- /help → Список команд и инструкции.\n"
                         "- /add (сумма) → добавление кнопки\n"
                         "- /link → ссылка на бота")
    help_message: str = ("- /start → Приветственное сообщение.\n"
                         "- /help → Список команд и инструкции.\n")
    def appeal_message(self, name):
        start_message: str = f"Доброго времени суток {name}"
        return start_message


@dataclass
class Link:
    tg_id: str

    @property
    def link(self) -> str:
        return f'https://t.me/vceXyuHia_bot?start={self.tg_id}'

@dataclass
class Sum:
    quantity: float

    @property
    def formatted_sum(self) -> str:
        return f"{self.quantity:.2f} RUB"