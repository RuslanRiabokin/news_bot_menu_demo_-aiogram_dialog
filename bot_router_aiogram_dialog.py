from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs

from bot_create_news_aiogram_dialog import start_dialog
from states_class_aiogram_dialog import MainDialogSG
from subscription_list_aiogram_dialog import current_subscriptions_dialog
from edit_subscriptions_aiogram_dialog import edit_subscription_dialog

basic_commands_router = Router()


# Хендлер для команди /start
@basic_commands_router.message(CommandStart())
async def command_start_handler(message: Message, dialog_manager: DialogManager):
    """Запускає перший діалог при команді /start"""
    await dialog_manager.start(MainDialogSG.welcome, mode=StartMode.RESET_STACK)


async def register_routes(dp: Dispatcher):
    # Реєстрація роутерів та діалогів
    dp.include_router(basic_commands_router)
    dp.include_routers(start_dialog, current_subscriptions_dialog, edit_subscription_dialog)
    setup_dialogs(dp)  # Налаштування системи діалогів