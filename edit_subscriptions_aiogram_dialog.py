from datetime import date
from typing import List

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Group, Calendar
from aiogram_dialog.widgets.text import Const, Format

from states_class_aiogram_dialog import EditSubscriptions, SecondDialogSG
from subscription_list_aiogram_dialog import go_start
from custom_calendar import CustomCalendar, on_date_selected, selection_getter


# Обробники кнопок у меню редагування
async def edit_publication_time(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("🕒 Час публікації буде змінено.")

async def pause_publication(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("⏸ Публікацію призупинено.")

async def add_poll(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("📊 Опитування додано.")

async def send_cat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Ось ваш котик! 🐈")
    await callback.answer()

# Обробник вибору мови
async def on_language_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    selected_language = button.widget_id
    message = MESSAGES.get(selected_language, f"Selected language: {selected_language}")
    await callback.message.answer(message)
    await dialog_manager.switch_to(EditSubscriptions.edit)

async def select_language(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(EditSubscriptions.select_language)

async def back_to_subscription_details(callback: CallbackQuery, button: Button,
                                       dialog_manager: DialogManager):
    await dialog_manager.done()
    await dialog_manager.switch_to(SecondDialogSG.second)


"""# Обробник вибору дати
async def on_date_selected2(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):

    selected_dates: List[date] = manager.dialog_data.setdefault("selected_dates", [])

    if selected_date in selected_dates:
        selected_dates.remove(selected_date)  # Видаляємо, якщо дата вже була обрана
    else:
        selected_dates.append(selected_date)  # Додаємо нову дату

    # Оновлюємо віджет для відображення обраних дат
    await widget.manager().dialog().update()"""

# Обробник завершення вибору дат
async def finish_selection(callback: CallbackQuery, button: Button, manager: DialogManager):
    """Завершення вибору дат та виведення остаточного списку."""
    selected_dates = manager.dialog_data.get("selected_dates", [])
    dates_text = ", ".join([str(d) for d in selected_dates])
    await callback.message.answer(f"Ваш остаточний вибір: {dates_text}")
    await manager.done()

# Словник повідомлень різними мовами
MESSAGES = {
    "uk": "Ви обрали мову: Українська",
    "en": "You selected the language: English",
    "ru": "Вы выбрали: Русский",
    "de": "Sie haben die Sprache gewählt: Deutsch",
}

# Вікно для вибору мови
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
    Button(Const("Назад"), id="back_to_edit",
           on_click=lambda c, b, d: d.switch_to(EditSubscriptions.edit)),
    state=EditSubscriptions.select_language,
)

# Головне вікно редагування підписки
edit_subscription_window = Window(
    Const("<b>Опції редагування підписки</b>\n"),
    Row(
        Button(Const("Змінити час публікації 🕒"), id="change_time",
               on_click=edit_publication_time),
        Button(Const("Призупинити публікацію ⏸"), id="pause_publication", on_click=pause_publication),
    ),
    Row(
        Button(Const("Додати опитування 📊"), id="add_poll", on_click=add_poll),
        Button(Const("Вислати котика 🐈"), id="send_cat", on_click=send_cat),
    ),
    Row(
        Button(Const("Вибрати мову"), id="select_language", on_click=select_language),
Button(Const("Календар"), id="open_calendar", on_click=lambda c, b, d: d.switch_to(EditSubscriptions.calendar)),
    ),
    Button(Const("Повернутись назад"), id="back_button", on_click=back_to_subscription_details),
    Button(Const("Повернутися до початкового меню"), id="button_start", on_click=go_start),
    state=EditSubscriptions.edit,
)


# Вікно з кастомним календарем
calendar_window = Window(
    Const("<b>Оберіть дати:</b>"),
    Format("\nSelected: {selected}", when=F["selected"]),
    Format("\nNo dates selected", when=~F["selected"]),
    CustomCalendar(
        id="calendar",
        on_click=on_date_selected,
    ),
    Button(Const("Завершити вибір"), id="finish", on_click=finish_selection),
    Button(Const("Назад"), id="back_to_edit", on_click=lambda c, b, d: d.switch_to(EditSubscriptions.edit)),
    state=EditSubscriptions.calendar,
    getter=selection_getter
)


# Об'єднання вікон у діалог
edit_subscription_dialog = Dialog(
    edit_subscription_window,
    select_language_window,
    calendar_window,
)
