# bot_router_aiogram_dialog.py
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


async def clear_previous_messages(dialog_manager: DialogManager, message: Message):
    """Видаляє всі повідомлення та завершує активний діалог."""
    try:
        # Завершуємо активний діалог, якщо він є
        await dialog_manager.reset_stack()
    except Exception as e:
        print(f"Помилка при скиданні діалогу: {e}")

    # Видаляємо останні повідомлення (наприклад, останні 10)
    chat_id = message.chat.id
    for i in range(10):  # Кількість повідомлень для видалення
        try:
            await message.bot.delete_message(chat_id, message.message_id - i)
        except Exception:
            continue  # Пропускаємо помилки, якщо повідомлення вже видалено

# Хендлер для команди /start
@basic_commands_router.message(CommandStart())
async def command_start_handler(message: Message, dialog_manager: DialogManager):
    """Запускає перший діалог при команді /start"""
    await clear_previous_messages(dialog_manager, message)
    await dialog_manager.start(MainDialogSG.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)

# Хендлер для команди /menu
@basic_commands_router.message(Command("menu"))
async def menu_command_handler(message: Message, dialog_manager: DialogManager):
    """Хендлер для команди /menu, що відкриває вікно з меню підписок"""
    await clear_previous_messages(dialog_manager, message)
    await dialog_manager.start(MainDialogSG.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)

@basic_commands_router.message()
async def unknown_command_handler(message: Message, dialog_manager: DialogManager):
    """Повідомляє про невідому команду та одразу відкриває меню."""
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
    dp.include_routers(start_dialog, current_subscriptions_dialog, edit_subscription_dialog)
    setup_dialogs(dp)  # Налаштування системи діалогів
