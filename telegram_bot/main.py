import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
from aiogram.fsm.storage.memory import SimpleEventIsolation
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv("./telegram_bot/.env")
TOKEN = os.getenv("API") or "DEFAULT_API_TOKEN"


bot = Bot(TOKEN)


class RegisterScene(Scene, state="register"):
    pass
    

register_router = Router(name=__name__)
register_router.message.register(RegisterScene.as_handler(), Command("register"))


@register_router.message(Command("start"))
async def command_start(message : Message, scenes : ScenesManager):
    await scenes.close()
    await message.answer(
        "Здравствуйте! Это бот для получения расписания ФПМИ в удобном виде. Для начала использования введите команду /register",
        reply_markup=ReplyKeyboardRemove()
    )


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()    
    )
    dispatcher.include_router(register_router)
    
    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(RegisterScene)
    return dispatcher

    
async def main() -> None:
    commands = [
        BotCommand(command="start", description="старт бота"),
        BotCommand(command="register", description="регистрация и ввод данных про себя"),
        BotCommand(command="modify", description="изменение данных про себя"),
        BotCommand(command="exit", description="выход из бота и удаление данных про себя")
    ]
    await bot.set_my_commands(commands=commands)
    scheduler = AsyncIOScheduler()
    dp = create_dispatcher()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
    
    
    
# async def send_aps_message(chat_id: int):
#     await bot.send_message(chat_id, "This message was scheduled with APScheduler!")

# @dp.message_handler(commands=['schedule_aps'])
# async def schedule_aps_message(message: types.Message):
#     scheduler.add_job(
#         send_aps_message,
#         'date',
#         run_date=datetime.now() + timedelta(seconds=10),
#         args=[message.chat.id]
#     )
#     await message.reply("APScheduler message scheduled for 10 seconds from now.")

# if __name__ == '__main__':
#     scheduler.start()
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)