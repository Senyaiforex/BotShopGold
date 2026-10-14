from dataclasses import dataclass
import os


@dataclass(frozen=True)
class HandlersText:
    welcome_text: str = ("*Добро пожаловать!*\n\n"
                         "В нашем боте Вы можете купить голду для игры Standoff 2 за рубли.\n"
                         "Нажмите на кнопку «Купить» для продолжения")
    buy_menu_text: str = ("Отправьте сообщение, сколько Вам необходимо купить голды?\n"
                          "Текущий курс 1 к {rate}")

txt_handlers = HandlersText()