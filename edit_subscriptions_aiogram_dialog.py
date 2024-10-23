from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Group
from aiogram_dialog.widgets.text import Const
from states_class_aiogram_dialog import EditSubscriptions, SecondDialogSG
from subscription_list_aiogram_dialog import go_start

# Обработчики действий с кнопками
async def edit_publication_time(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("🕒 Час публікації буде змінено.")

async def pause_publication(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("⏸ Публікацію призупинено.")

async def add_poll(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("📊 Опитування додано.")

async def send_cat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Ось ваш котик! 🐈")
    await callback.answer()

# Словарь переводов сообщений
MESSAGES = {
    "uk": "Ви обрали мову: Українська",
    "en": "You selected the language: English",
    "ru": "Вы выбрали: Русский",
    "de": "Sie haben die Sprache gewählt: Deutsch",
}

async def on_language_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработка выбора языка с выводом сообщения на выбранном языке."""
    selected_language = button.widget_id  # ID кнопки как код языка
    message = MESSAGES.get(selected_language, f"Selected language: {selected_language}")  # Берем сообщение или дефолтное

    await callback.message.answer(message)  # Отправляем сообщение на нужном языке
    await dialog_manager.switch_to(EditSubscriptions.edit)  # Переход обратно в меню

async def select_language(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(EditSubscriptions.select_language)

async def back_to_subscription_details(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await dialog_manager.switch_to(SecondDialogSG.second)

# Окно выбора языка
select_language_window = Window(
    Const("<b>Виберіть мову:</b>"),
    Group(
        Row(
            Button(Const("Українська"), id="uk", on_click=on_language_selected),
            Button(Const("English"), id="en", on_click=on_language_selected),
        ),
        Row(
            Button(Const("Русский"), id="ru", on_click=on_language_selected),
            Button(Const("Deutsch"), id="de", on_click=on_language_selected),
        ),
    ),
    Button(Const("Назад"), id="back_to_edit", on_click=lambda c, b, d: d.switch_to(EditSubscriptions.edit)),
    state=EditSubscriptions.select_language,
)

# Главное окно редактирования подписки
edit_subscription_window = Window(
    Const("<b>Опції редагування підписки</b>\n"),
    Row(
        Button(Const("Змінити час публікації 🕒"), id="change_time", on_click=edit_publication_time),
        Button(Const("Призупинити публікацію ⏸"), id="pause_publication", on_click=pause_publication),
    ),
    Row(
        Button(Const("Додати опитування 📊"), id="add_poll", on_click=add_poll),
        Button(Const("Вислати котика 🐈"), id="send_cat", on_click=send_cat),
    ),
    Row(
        Button(Const("Вибрати мову"), id="select_language", on_click=select_language),
    ),
    Button(Const("Повернутись назад"), id="back_button", on_click=back_to_subscription_details),
    Button(Const("Повернутися до початкового меню"), id="button_start", on_click=go_start),
    state=EditSubscriptions.edit,
)

# Объединение всех окон в один диалог
edit_subscription_dialog = Dialog(
    edit_subscription_window,
    select_language_window,
)
