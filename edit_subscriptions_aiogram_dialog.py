from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from states_class_aiogram_dialog import EditSubscriptions, SecondDialogSG
from subscription_list_aiogram_dialog import go_start


async def edit_publication_time(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обробка натискання на 'Змінити час публікації'."""
    await callback.message.answer("🕒 Час публікації буде змінено.")

async def pause_publication(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обробка натискання на 'Призупинити публікацію'."""
    await callback.message.answer("⏸ Публікацію призупинено.")

async def add_poll(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обробка натискання на 'Додати опитування'."""
    await callback.message.answer("📊 Опитування додано.")


async def send_cat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Відправляє повідомлення з текстом про котика."""
    await callback.message.answer("Ось ваш котик! 🐈")
    await callback.answer()  # Закриваємо callback


async def back_to_subscription_details(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Повернення до деталей підписки."""
    await dialog_manager.done()  # Завершити поточний діалог
    await dialog_manager.switch_to(state=SecondDialogSG.second)  # Перехід до другого вікна з підписками



# Визначення діалогу з кнопками редагування
edit_subscription_dialog = Dialog(
    Window(
        Const("<b>Опції редагування підписки</b>\n"),
        Row(
            Button(Const("Змінити час публікації 🕒"), id="change_time", on_click=edit_publication_time),
            Button(Const("Призупинити публікацію ⏸"), id="pause_publication", on_click=pause_publication),
        ),
        Row(
            Button(Const("Додати опитування 📊"), id="add_poll", on_click=add_poll),
            Button(Const("Вислати котика 🐈"), id="send_cat", on_click=send_cat),
        ),
        Button(Const("Повернутись назад"), id="back_button", on_click=back_to_subscription_details),
        Button(Const('Повернутися до початкового меню'), id='button_start', on_click=go_start),
        state=EditSubscriptions.edit,
    )
)
