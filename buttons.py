from aiogram import types

inbuttons = ['Изменить выбранное меню', 'Новый день - новое меню!']


# \U0000270F  \U000027A1
def set_keyboard(args: list | str) -> types.ReplyKeyboardMarkup:
    """
    Создаёт тип ReplyKeyboardMarkup. На кнопку "Авторизация" добавляется запрос контакта
    :param args: список или строка, которая будет передана в наименование кнопки
    :return:
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button in args:
        if button == 'Авторизация':
            keyboard.add(types.KeyboardButton(text=button, request_contact=True))
        else:
            keyboard.add(types.KeyboardButton(text=button))
    return keyboard


def set_inlineKeyboard(args) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for button in args:
        keyboard.add(types.InlineKeyboardButton(text=button, callback_data=button))
    return keyboard
