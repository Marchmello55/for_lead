import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
import traceback
from typing import Any, Dict
from config_data.config import Config, load_config
from handlers import start, link, other_handlers, add, help
from database.models import async_main
# Инициализируем logger
logger = logging.getLogger(__name__)


async def main():
    await async_main()
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        # filename="py_log.log",
        # filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Регистрируем router в диспетчере
    dp.include_router(start.router)
    dp.include_router(link.router)
    dp.include_routers(add.router, help.router)
    dp.include_router(other_handlers.router)


    @dp.error()
    async def error_handler(event: ErrorEvent, data: Dict[str, Any]):
        logger.critical("Критическая ошибка: %s", event.exception, exc_info=True)
        await bot.send_message(chat_id=config.tg_bot.support_id,
                               text=f'{event.exception}')
        formatted_lines = traceback.format_exc()
        text_file = open('error.txt', 'w')
        text_file.write(str(formatted_lines))
        text_file.close()


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())