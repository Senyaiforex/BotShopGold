from aiogram.fsm.state import StatesGroup, State


class ClientStates(StatesGroup):
    """
    Состояния для работы с клиентами
    """
    COUNT_GOLD = State()
    WAIT_SCREEN = State()


class AdminStates(StatesGroup):
    """
    Состояния для работы с другими данными от клиента
    """
    WAIT_RATE = State()


