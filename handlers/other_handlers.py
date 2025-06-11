from aiogram.types import CallbackQuery
from aiogram import F, Router, Bot



from datetime import datetime
from database import requests as rq
from config_data.config import Config, load_config
import logging

router = Router()
config: Config = load_config()

@router.callback_query(F.data.startswith('button_'))
async def select_type_order(callback: CallbackQuery, bot: Bot):
    if await rq.get_button_id(int(callback.data.split('_')[-1])) == rq.Access.busy:
        await callback.message.answer("выберите другой тариф, этот занят")
        await callback.answer()
        return
    await callback.message.answer("Спасибо!\n"
                                  "Ваша заявка передана оператору.\n"
                                  "Он свяжется с вами в течение 5 минут.\n"
                                  "Будьте на связи.")
    await callback.answer()
    await rq.change_access_button(f"{callback.data.split('_')[1]}", rq.Type_button.inline)
    if callback.message.from_user.username:
        await bot.send_message(chat_id=int(config.tg_bot.support_id), text=f"{datetime.now()}\n"
                           f"@{callback.from_user.username}\n"
                           f"{callback.data.split('_')[1]}")
    else:
        await bot.send_message(chat_id=int(config.tg_bot.support_id), text=f"{datetime.now()}\n"
                            f'<a href="tg://user?id={callback.from_user.id}">{callback.message.from_user.first_name}</a>'
                            f"{callback.data.split('_')[1]}", parse_mode="HTML")