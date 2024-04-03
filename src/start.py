import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


from config import Config as config
from handlers import router


bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(router)

async def on_startup_echo():
    text = 'Bot is started'
    await bot.send_message(chat_id=config.admin_id,
                           text=text)


async def on_shutdown_echo():
    text = 'Bot is shutdown'
    await bot.send_message(chat_id=config.admin_id,
                           text=text)


async def main():
    print('Start bot')
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        dp.startup.register(on_startup_echo)
        dp.shutdown.register(on_shutdown_echo)
        await asyncio.gather(dp.start_polling(bot=bot))
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
