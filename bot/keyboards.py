from typing import Any

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)


async def buy_keyboard() -> InlineKeyboardMarkup:
    """
    Функция создаёт inline-кнопки для стартового сообщения
    :return: InlineKeyboardMarkup
    """
    menu_but = [InlineKeyboardButton(text='Купить',
                                     callback_data='buy')]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[menu_but])
    return keyboard

async def after_buy_keyboard() -> InlineKeyboardMarkup:
    """
    Функция создаёт inline-кнопки в меню покупки и ввода голды
    :return: InlineKeyboardMarkup
    """
    but_1 = [InlineKeyboardButton(text='Продолжить',
                                     callback_data='payment')]
    but_2 = [InlineKeyboardButton(text='Изменить',
                                     callback_data='buy')]
    but_3 = [InlineKeyboardButton(text='Назад',
                                     callback_data='menu')]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[but_1, but_2, but_3])
    return keyboard

async def admin_after_pay(user_id: int) -> InlineKeyboardMarkup:
    """
    Функция создаёт inline-кнопки для администратора после оплаты пользователем
    :return:
    """
    but_1 = [InlineKeyboardButton(text="Подтвердить", callback_data=f"solution-{user_id}-yes")]
    but_2 = [InlineKeyboardButton(text="Отклонить", callback_data=f"solution-{user_id}-no")]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[but_1, but_2])
    return keyboard

async def admin_menu() -> InlineKeyboardMarkup:
    """
    Функция создаёт inline-кнопки для администратора после оплаты пользователем
    :return:
    """
    but_1 = [InlineKeyboardButton(text="Изменить курс", callback_data=f"change_rate")]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[but_1])
    return keyboard
async def admin_back_menu() -> InlineKeyboardMarkup:
    """
    Функция создаёт inline-кнопки для администратора после оплаты пользователем
    :return:
    """
    but_1 = [InlineKeyboardButton(text="Назад", callback_data=f"admin-menu")]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[but_1])
    return keyboard