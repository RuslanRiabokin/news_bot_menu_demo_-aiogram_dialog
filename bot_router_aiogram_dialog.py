import asyncio

from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs, ShowMode

from bot_create_news_aiogram_dialog import start_dialog
from states_class_aiogram_dialog import MainDialogSG
from subscription_list_aiogram_dialog import current_subscriptions_dialog
from edit_subscriptions_aiogram_dialog import edit_subscription_dialog

# Ініціалізація Router
basic_commands_router = Router()
menu_router = Router()  # Окремий роутер для команди /menu

# Хендлер для команди /start
@basic_commands_router.message(CommandStart())
async def command_start_handler(message: Message, dialog_manager: DialogManager):
    """Запускає перший діалог при команді /start"""
    await dialog_manager.start(MainDialogSG.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)
    await message.delete()

# Хендлер для команди /menu
@menu_router.message(Command("menu"))
async def menu_command_handler(message: Message, dialog_manager: DialogManager):
    """Хендлер для команди /menu, що відкриває вікно з меню підписок"""
    await dialog_manager.start(MainDialogSG.menu, show_mode=ShowMode.DELETE_AND_SEND)
    await message.delete()


@basic_commands_router.message()
async def unknown_command_handler(message: Message, dialog_manager: DialogManager):
    """Сообщает о неизвестной команде и сразу открывает меню."""
    reply = await message.answer(
        "Ця команда не відома, виберіть команду з меню або введіть /menu."
    )
    await asyncio.sleep(3)
    await reply.delete()
    await message.delete()
    await dialog_manager.start(
        state=MainDialogSG.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND
    )



async def register_routes(dp: Dispatcher):
    # Реєстрація роутерів та діалогів
    dp.include_router(basic_commands_router)
    dp.include_router(menu_router)  # Додаємо роутер для /menu
    dp.include_routers(start_dialog, current_subscriptions_dialog, edit_subscription_dialog)
    setup_dialogs(dp)  # Налаштування системи діалогів
