import operator
import re

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Row, Column, Multiselect
from aiogram_dialog.widgets.text import Const, Format

from states_class_aiogram_dialog import MainDialogSG, SecondDialogSG

# Вітальний текст
welcome_text = (
    "Вас вітає новинний бот 📰!\n\n"
    "Наразі завдяки нашому боту ви можете:\n\n"
    "1️⃣ Створити нову підписку ✅\n"
    "2️⃣ Переглянути список підписок 📋\n"
    "➕ Додати опитування до новини\n"
    "␡ Видалити опитування\n"
    "␡ Видалити підписку\n"
    "♻️ Відновити підписку\n"
    "📰 Змінити тип відображення новин\n"
    "🧾🚀 Почати публікацію\n\n"
    "Для доступу до інших функцій натисніть кнопку меню нижче."
)

async def go_second_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Перемикається на перше вікно другого діалогу"""
    await dialog_manager.start(state=SecondDialogSG.first)


async def switch_to_first_subscription(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Перемикається на стан 'subscription' у першому діалозі"""
    await dialog_manager.switch_to(state=MainDialogSG.start)


async def switch_to_first_lists(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Перемикається на стан вибору тем у першому діалозі"""
    await dialog_manager.switch_to(state=MainDialogSG.new_subscription)


async def return_to_subscription(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Повертається до стану 'subscription' у першому діалозі"""
    await dialog_manager.switch_to(state=MainDialogSG.start)


async def get_topics(dialog_manager: DialogManager, **kwargs):
    """Повертає список тем для вибору в діалозі новин"""
    topics = [
        ("IT", '1'),
        ("Дизайн", '2'),
        ("Наука", '3'),
        ("Суспільство", '4'),
        ("Культура", '5'),
        ("Мистецтво", '6'),
    ]
    return {"topics": topics}


def news_check(text: str) -> str:
    """Перевірка тексту на наявність змісту і довжини"""
    stripped_text = text.strip()  # Прибираємо пробіли
    # Перевірка, що текст містить хоча б одну літеру та має правильну довжину
    if not stripped_text or not re.search(r'[a-zA-Zа-яА-Я]', stripped_text):
        raise ValueError("Введіть не порожнє повідомлення або текст, що містить літери.")
    if len(stripped_text) < 2:
        raise ValueError("Текст має бути не коротший за дві літери.")
    if len(stripped_text) > 20:
        raise ValueError("Текст не повинен перевищувати 20 символів.")
    return stripped_text


async def correct_news_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    """Хендлер, який спрацює, якщо користувач ввів коректну новину"""
    await message.answer(text=f"Ви ввели новину: {text}")
    # Перемикаємося назад на головне меню підписок
    await dialog_manager.switch_to(state=MainDialogSG.start, show_mode=ShowMode.SEND)


async def error_news_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    """Хендлер, який спрацює на ввід некоректної новини"""
    await message.answer(text=str(error))  # Виводимо повідомлення про помилку


async def confirm_selected_topics(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Підтверджує вибір новин і виводить повідомлення про підписку"""
    # Видаляємо старе повідомлення з текстом "Оберіть теми новин"
    await callback.message.delete()

    # Отримуємо вибрані теми
    multi_topics_widget = dialog_manager.find("multi_topics")
    selected_topics = multi_topics_widget.get_checked()

    # Викликаємо get_topics, щоб отримати список всіх тем
    topics_data = await get_topics(dialog_manager)
    all_topics = topics_data["topics"]  # Список тем у форматі [("IT", '1'), ("Дизайн", '2'), ...]

    # Відбираємо назви тем за їх ідентифікаторами
    selected_topic_names = [name for name, id in all_topics if id in selected_topics]

    if selected_topic_names:
        topics_list = ", ".join(selected_topic_names)
        await callback.message.answer(f"Ви підписалися на наступні новини: {topics_list}", disable_notification=True)
    else:
        await callback.message.answer("Ви не обрали жодної теми новин.", disable_notification=True)

    # Очищуємо стек і повертаємося до стартового меню з використанням show_mode=ShowMode.SEND
    await dialog_manager.switch_to(state=MainDialogSG.start, show_mode=ShowMode.SEND)


start_dialog = Dialog(
    # Привітальне вікно
    Window(
        Const("Вас вітає новинний бот 📰!\n\n"
    "Наразі завдяки нашому боту ви можете:\n\n"
    "1️⃣ Створити нову підписку ✅\n"
    "2️⃣ Переглянути список підписок 📋\n"
    "➕ Додати опитування до новини\n"
    "␡ Видалити опитування\n"
    "␡ Видалити підписку\n"
    "♻️ Відновити підписку\n"
    "📰 Змінити тип відображення новин\n"
    "🧾🚀 Почати публікацію\n\n"
    "Для доступу до інших функцій натисніть кнопку меню нижче."),
        Row(
            Button(Const('Перейти до меню'), id='go_menu', on_click=switch_to_first_subscription),  # Кнопка для переходу в меню
        ),
        state=MainDialogSG.welcome
    ),
    # Вікно з меню підписок
    Window(
        Const('<b>Ви знаходитесь в меню Підписок</b>\n'),
        Const('Ви можете перемикатися між вікнами поточного діалогу або перейти до нового 👇'),
        Row(
            Button(Const('Створити підписку'), id='w_second', on_click=switch_to_first_lists),
        ),
        Row(
            Button(Const('Переглянути Список підписок ▶️'), id='go_second_dialog', on_click=go_second_dialog),
        ),
        state=MainDialogSG.start
    ),
    # Вікно з вибором тем
    Window(
        Const('<b>Оберіть теми новин:</b>'),
        Column(
            Multiselect(
                checked_text=Format('✔️ {item[0]}'),  # Форматування вибраної теми
                unchecked_text=Format(' {item[0]}'),  # Форматування невибраної теми
                id='multi_topics',
                item_id_getter=operator.itemgetter(1),
                items="topics",
            ),
        ),
        Row(Button(Const('Підтвердити вибрані новини 📝'),
                   id='confirm_topics', on_click=confirm_selected_topics)),  # Кнопка підтвердження вибору
        Row(Button(Const('Введіть свою новину 📝'),
                   id='enter_news', on_click=lambda callback, button,
                    dialog_manager: dialog_manager.switch_to(
                    state=MainDialogSG.enter_news))),  # Кнопка для вводу новини
        Row(
            Button(Const('У 2-й діалог ▶️'), id='go_second_dialog', on_click=go_second_dialog),
            Button(Const('Скасувати'), id='cancel_to_subscription', on_click=return_to_subscription)  # Кнопка Скасувати
        ),
        state=MainDialogSG.new_subscription,
        getter=get_topics  # Отримання списку тем
    ),
    # Вікно для вводу новини
    Window(
        Const("Будь ласка, введіть вашу новину:"),
        TextInput(
            id='news_input',
            type_factory=news_check,
            on_success=correct_news_handler,
            on_error=error_news_handler,
        ),
        state=MainDialogSG.enter_news  # Стан для вводу новини
    )
)
