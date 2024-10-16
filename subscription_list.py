import logging
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Row
from aiogram_dialog.widgets.text import Const, Format

from database import AsyncDatabase
from states import MainDialogSG, SecondDialogSG, EditSubscriptions


# Ініціалізація бази даних та логування
db = AsyncDatabase()
logging.basicConfig(level=logging.INFO)


async def close_second_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Закриває другий діалог."""
    await dialog_manager.done()


async def switch_to_second_lists(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Перехід на друге вікно другого діалогу."""
    await dialog_manager.switch_to(state=SecondDialogSG.second)


async def handle_subscription_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                    item_id: str):
    """Обробляє натискання на кнопку підписки та зберігає item_id і topic_name у контексті."""
    # Приводимо item_id до цілого числа
    try:
        item_id = int(item_id)
    except ValueError:
        logging.error(f"Неправильний формат item_id: {item_id}")
        return

    # Отримуємо список підписок із контексту
    subscriptions = dialog_manager.dialog_data.get("subscriptions", [])

    # Шукаємо підписку за item_id (sub_id)
    selected_subscription = next((sub for sub in subscriptions if sub[0] == item_id), None)

    if selected_subscription:
        topic_name = selected_subscription[1]  # Назва підписки
        dialog_manager.dialog_data["item_id"] = item_id
        dialog_manager.dialog_data["topic_name"] = topic_name
        logging.info(f"Обрана підписка: {selected_subscription}")
    else:
        logging.error(f"Підписку з id {item_id} не знайдено!")

    await dialog_manager.switch_to(state=SecondDialogSG.second)


async def subscription_getter(dialog_manager: DialogManager, **kwargs):
    """Отримує підписки для користувача та логує їх."""
    user_id = dialog_manager.event.from_user.id
    logging.info(f"Отримуємо підписки для користувача з ID {user_id}")

    try:
        subscriptions = await db.get_subscriptions(user_id)
        dialog_manager.dialog_data["subscriptions"] = subscriptions
        logging.info(f"Підписки: {subscriptions}")  # Логуємо дані

        # Генеруємо кнопки для кожної підписки
        buttons = [
            (f"{topic_name} - {channel_name}", sub_id)
            for sub_id, topic_name, channel_name, _ in subscriptions
        ]

        return {"subscriptions": buttons}
    except Exception as e:
        logging.error(f"Помилка під час отримання підписок: {e}")
        return {"subscriptions": []}


async def second_window_getter(dialog_manager: DialogManager, **kwargs):
    """Передає item_id та topic_name з контексту для відображення у другому вікні."""
    item_id = dialog_manager.dialog_data.get("item_id", "Невідома підписка")
    topic_name = dialog_manager.dialog_data.get("topic_name", "Невідома підписка")
    logging.info(f"Друге вікно: item_id={item_id}, topic_name={topic_name}")  # Логуємо значення
    return {"item_id": item_id, "topic_name": topic_name}


async def back_to_subscriptions(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Повертає користувача до вікна з підписками."""
    await dialog_manager.switch_to(state=SecondDialogSG.first)


async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Повертає до початкового меню."""
    await dialog_manager.start(state=MainDialogSG.start, mode=StartMode.RESET_STACK)


async def delete_subscription_message(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Виводить повідомлення про видалення підписки."""
    item_id = dialog_manager.dialog_data.get("item_id", "Невідомий ID")
    topic_name = dialog_manager.dialog_data.get("topic_name", "Невідома підписка")
    # Логуємо подію видалення
    logging.info(f"Повідомлення про видалення: {item_id} - {topic_name}")
    # Виводимо повідомлення користувачу
    await callback.message.answer(
        f"✅ Ви видалили підписку: <b>{item_id}</b> - <b>{topic_name}</b>"
    )
    # Повернення до попереднього вікна з підписками
    await dialog_manager.switch_to(state=SecondDialogSG.first)


async def switch_to_edit_options(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Перехід до вікна редагування підписок."""
    await dialog_manager.start(state=EditSubscriptions.edit, mode=StartMode.NORMAL)



# Визначення діалогу з підписками
current_subscriptions_dialog = Dialog(
    Window(
        Const('<b>Ви знаходитесь у меню ваших підписок!</b>\n'),
        ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id='subscriptions',
                item_id_getter=lambda x: x[1],
                items='subscriptions',
                on_click=handle_subscription_click,
            ),
            id='subscriptions_group',
            width=1,
            height=4,
        ),
        Button(Const('Скасувати'), id='button_cancel', on_click=close_second_dialog),
        state=SecondDialogSG.first,
        getter=subscription_getter  # Джерело даних для першого вікна
    ),
    Window(
        Format("<b>Меню новин:</b>\n <b>Ви обрали підписку: {item_id} {topic_name}</b>"),
        Row(
            Button(Const('Редагувати 📝'), id='edit_button', on_click=switch_to_edit_options),
            Button(Const('Видалити 📝'), id='delete_button', on_click=delete_subscription_message),
        ),
        Button(Const('Скасувати'), id='button_cancel', on_click=back_to_subscriptions),
        Button(Const('Повернутися до початкового меню'), id='button_start', on_click=go_start),
        state=SecondDialogSG.second,
        getter=second_window_getter  # Джерело даних для другого вікна
    )
)
