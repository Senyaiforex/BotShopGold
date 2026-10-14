from contextlib import suppress

from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import *
from text_static import *
from helpers import *
from states import ClientStates, AdminStates
router = Router()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ADMIN_ID = 8335431482

@router.message(F.photo)
async def get_photo_id(message: types.Message):
    await message.answer(
        message.photo[-1].file_id
    )

@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """
    Основная функция для начала работы с ботом
    :param message:
    :param state: FSMContext
    :return:
    """
    await state.clear()
    await message.answer_photo(
            caption=txt_handlers.welcome_text,
            reply_markup=await buy_keyboard(),
            parse_mode='Markdown',
            photo="AgACAgIAAxkBAANTas_RXT0-z5D9uGDBA_mjE_vS2OcAAoYfaxsx44FK6XthOBEkvrcBAAMCAAN5AAM9BA"
    )

@router.message(Command("admin"))
async def start_command(message: types.Message, state: FSMContext):
    """
    Основная функция для начала работы с ботом
    :param message:
    :param state: FSMContext
    :return:
    """
    await state.clear()
    if message.from_user.id != ADMIN_ID:
        return
    rate = await get_value("rate")
    await message.answer(
            text=f"Текущий курс покупки голды - 1 к {rate}",
            reply_markup=await admin_menu(),
            parse_mode='Markdown'
    )
@router.callback_query(lambda c: c.data == 'menu')
async def menu_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Меню» или «назад»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.answer()
    await state.clear()
    with suppress(AiogramError):
        await callback_query.message.delete()
    await callback_query.message.answer_photo(caption=txt_handlers.welcome_text,
                                              photo="AgACAgIAAxkBAANTas_RXT0-z5D9uGDBA_mjE_vS2OcAAoYfaxsx44FK6XthOBEkvrcBAAMCAAN5AAM9BA",
                                        reply_markup=await buy_keyboard(), parse_mode='Markdown')

@router.callback_query(lambda c: c.data == 'admin-menu')
async def admin_menu_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Меню» или «назад»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.answer()
    await state.clear()
    rate = await get_value("rate")
    try:
        await callback_query.message.edit_text(
                text=f"Текущий курс покупки голды - 1 к {rate}",
                reply_markup=await admin_menu(),
                parse_mode='Markdown'
        )
    except AiogramError as ex:
        await callback_query.message.answer(
                text=f"Текущий курс покупки голды - 1 к {rate}",
                reply_markup=await admin_menu(),
                parse_mode='Markdown'
        )
@router.callback_query(lambda c: c.data == 'buy')
async def buy_for_user(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Купить»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.answer()
    await state.clear()
    rate = await get_value("rate")
    text = txt_handlers.buy_menu_text.format(rate=rate)
    try:
        await callback_query.message.edit_text(text=text, parse_mode='Markdown')
    except AiogramError:
        await callback_query.message.answer(text=text, parse_mode='Markdown')
    await state.set_state(ClientStates.COUNT_GOLD)

@router.message(ClientStates.COUNT_GOLD, F.content_type == 'text')
async def sum_gold_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода количества покупаемого золота
    :param message:
    :param state:
    :return:
    """
    rate = await get_value("rate")
    try:
        count = int(message.text)
        result = int(count // rate)
        await message.answer(text=f"Итоговая стоимость: {result} рублей\n\n"
                                  f"Для перехода к оплате нажмите на кнопку «Продолжить»\n"
                                  f"Для перерасчета нажмите на кнопку «Изменить»\n"
                                  f"Для возвращения в главное меню «Назад»",
                             reply_markup=await after_buy_keyboard())
        await state.update_data(price=result, count=count)

    except (ValueError, AttributeError) as ex:
        await message.answer(text="Введите целое число. Пример: 10000")
        return

@router.callback_query(lambda c: c.data == 'payment')
async def user_payment(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки ввода суммы кредита
    :param callback_query:
    :param state:
    :return:
    """
    data = await state.get_data()
    price = data.get("price", None)
    count = data.get("count", None)
    if not price or not count:
        try:
            await callback_query.message.edit_text(text=txt_handlers.welcome_text,
                                                   reply_markup=await buy_keyboard())
        except AiogramError:
            await callback_query.message.answer(text=txt_handlers.welcome_text,
                                                reply_markup=await buy_keyboard())
        return

    text = (f"Для покупки {count} голды отправьте {price} рублей по следующим реквизитам:\n\n"
            f"<code>2202209200273794</code>\n"
            f"Сбербанк\n"
            f"Артём И.\n\n"
            f"У Вас есть 5 минут на оплату, после оплаты отправьте скриншот оплаты в чат")
    await state.set_state(ClientStates.WAIT_SCREEN)
    try:
        await callback_query.message.edit_text(text=text, parse_mode="HTML")
    except AiogramError:
        await callback_query.message.answer(text=text, parse_mode="HTML")
    return

@router.message(ClientStates.WAIT_SCREEN, F.content_type == 'photo')
async def send_screen_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки отправки скриншота оплаты
    :param message:
    :param state:
    :return:
    """
    data = await state.get_data()
    price = data.get("price", None)
    count = data.get("count", None)
    photo_id = message.photo[0].file_id
    text_for_admin = (f"Новая покупка {count} голды на сумму {price}\n\n"
                      f"Пользователь - @{message.from_user.username or message.from_user.full_name}")
    await message.bot.send_photo(photo=photo_id, chat_id=ADMIN_ID,
                                 caption=text_for_admin, reply_markup=await admin_after_pay(message.from_user.id))
    await message.answer_photo(caption="Ваша оплата проверяется! "
                                       "Пожалуйста, ожидайте окончания проверки\n\n"
                                       "Мы оповестим Вас по окончании проверки",
                               photo="AgACAgIAAxkBAANRas_RCl7rGlqln5iNFd3MTQkjbd"
                                     "cAAoIfaxsx44FK5qjMtuaYku4BAAMCAAN5AAM9BA")




@router.callback_query(lambda c: c.data.startswith('solution'))
async def admin_solution(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Проверка на стоп-факторы»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    _, user_id, type_sol = callback_query.data.split('-')
    dict_sol = {"yes": ["Оплата прошла успешно, свяжитесь с администратором для получения голды\n\n"
                       "@stormtight", "Оплата подтверждена, пользователь оповещён для связи с Вами"],
                "no": ["Администратор отклонил оплату. Если необходимо, то свяжитесь с ним для уточнения деталей\n\n"
                      "@stormtight", "Оплата отклонена"]}
    with suppress(Exception):
        await callback_query.message.delete_reply_markup()
    await callback_query.bot.send_message(chat_id=int(user_id), text=dict_sol[type_sol][0])
    await callback_query.message.answer(text=dict_sol[type_sol][1])
    await state.clear()


@router.callback_query(lambda c: c.data == 'change_rate')
async def buy_for_user(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Купить»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.answer()
    await state.clear()
    text = "Отправьте стоимость 1 голды в рублях"
    try:
        await callback_query.message.edit_text(text=text)
    except AiogramError:
        await callback_query.message.answer(text=text)
    await state.set_state(AdminStates.WAIT_RATE)

@router.message(AdminStates.WAIT_RATE, F.content_type == 'text')
async def rate_admin_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода количества покупаемого золота
    :param message:
    :param state:
    :return:
    """
    await message.delete()
    rate = await get_value("rate")
    try:
        count = int(message.text)
        await message.answer(text=f"Курс голды успешно изменён\n\n"
                                  f"Старый курс: {rate}\n"
                                  f"Новый курс: {count}",
                             reply_markup=await admin_back_menu())
        await set_value("rate", count)
    except (ValueError, AttributeError) as ex:
        await message.answer(text="Введите целое число. Пример: 60")
        return