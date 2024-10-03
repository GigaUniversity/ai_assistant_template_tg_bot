import asyncio

from source.bot import bot, dp
from source.lifespan import on_shutdown, on_startup


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await asyncio.gather(dp.start_polling(bot))
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
