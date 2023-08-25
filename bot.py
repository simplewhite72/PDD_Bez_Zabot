import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, question_text, inline_question_text, admin_text
from configs import config



# Запуск бота
async def main():
    bot = config.bot
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(inline_question_text.router)
    dp.include_router(question_text.router)
    dp.include_router(admin_text.router)
    
        
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.send_message(chat_id = config.admin_id, text = "Бот запущен!")

if __name__ == "__main__":
    asyncio.run(main())
