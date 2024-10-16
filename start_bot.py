import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from environs import Env

from bot_router import register_routes

logging.basicConfig(level=logging.INFO)

# Читання змінних оточення
env = Env()
env.read_env()

WEBAPP_HOST = env('WEB_SERVER_HOST', 'localhost')
WEBAPP_PORT = env.int('WEB_SERVER_PORT', 5000)
WEBHOOK_URL = env('BASE_WEBHOOK_URL') + "/webhook"
BOT_TOKEN = env('BOT_TOKEN_2')

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def on_startup():
    """Налаштування вебхуків"""
    result = await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {result}")

async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Webhook удалён и сессия закрыта")


async def main():
    """Налаштування сервера для роботи з aiohttp"""
    await register_routes(dp)
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    await on_startup()

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEBAPP_HOST, port=WEBAPP_PORT)
    await site.start()

    logging.info(f"Webhook URL: {WEBHOOK_URL}")
    logging.info(f"Server started on {WEBAPP_HOST}:{WEBAPP_PORT}")

    try:
        while True:
            await asyncio.sleep(3600)  # Запуск сервера
    finally:
        await on_shutdown()

if __name__ == '__main__':
    asyncio.run(main())
