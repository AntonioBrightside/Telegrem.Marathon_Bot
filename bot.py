from aiogram import Bot, Dispatcher, executor, types
from to_test.components_and_pairs import BREAKFAST, SUPPER, COMPONENTS
from buttons import set_keyboard, set_inlineKeyboard, inbuttons
from checker import answers_checker
from waiter import Waiter
import json


# To check. Delete after DB is connected
ACCCESS_PHONES = ['+79168755594', '+79296141965', '79168755594']  # TODO: протестировать и на PC и на мобилке вход

# Get data to bot access
with open(r'TB_settings.json', 'r') as f:
    settings = json.load(f)
    TOKEN = settings.get('Token')
    PAYMENT_TOKEN = settings.get('PayMaster_Test_TOKEN')

# Get bot access t.me/Diet_Marathon_Training_bot
bot = Bot(TOKEN)
dp = Dispatcher(bot)
answers = []


# Creating login keyboard
@dp.message_handler(commands=['start'])
async def login(message):
    await message.reply('Добро пожаловать. Доступ к данному боту имеют пользователи, которые оплатили курс. '
                        'Если вы входите в их число, нажмите кнопку "Авторизация" или "Стать участником", '
                        f'если хотите присоединиться ', reply_markup=set_keyboard(['Авторизация', 'Стать участником']))


# Handling the contact message from user and Welcome message after authentication
@dp.message_handler(content_types=['contact'])
async def contact(
        message):  # TODO: он не только должен сохранять, но и проверять (т.к. после оплаты пользователь все равно падает на уровень авторизации)
    if message.contact:
        if message.contact.user_id == message.from_user.id and message.contact['phone_number'] in ACCCESS_PHONES:
            print(
                message.contact)  # TODO: заменить на сохранение в БД. Возможно добавить first_name в текст при общении
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Добро пожаловать! Давайте подберем меню, исходя из ваших предпочтений по ингридиентам. Подберем на завтрак или ужин?',
                                   reply_markup=set_keyboard(['Завтрак', 'Ужин']))  # TODO: проверка в БД

        elif message.contact.user_id != message.from_user.id:
            await message.reply('Этот контакт принадлежит другому аккаунту')
        else:
            print(message.contact) # Заменить на БД или
            await message.reply('К сожалению, вас нет в нашей базе, поэтмоу предлагаем вам оплатить курс',
                                reply_markup=set_keyboard('Стать участником'))


# Handling "Стать участником" / "Завтрак" / "Ужин" conversation
@dp.message_handler(content_types=['text'])
async def breakfact(message):
    global answers
    if message.text == 'Стать участником':
        await message.reply("You're god damn right. Давайте начнем оплату")
        await bot.send_invoice(chat_id=message.from_user.id,
                               title='Подписка на бота',
                               description='Подписка на период прохождения марафона',
                               payload='test-payload',
                               provider_token=PAYMENT_TOKEN,
                               currency='rub',
                               prices=[types.LabeledPrice(label='Подписка на бота', amount=500 * 100)],
                               need_name=True,
                               need_phone_number=True,
                               need_email=True)

    elif message.text == 'Завтрак' or message.text == '/breakfast':
        answers.append(message.text)
        answers = answers_checker(answers)
        await message.reply('Из каких ингридиентов хотите собрать свой завтрак?'
                            'Не забывайте, что ингридиентов может быть больше, чем помещается на экране, '
                            'используйте scroll', reply_markup=set_keyboard(BREAKFAST))

    elif message.text == 'Ужин' or message.text == '/supper':
        answers.append(message.text)
        answers = answers_checker(answers)
        await message.reply('Из каких ингридиентов хотите собрать свой ужин?'
                            'Не забывайте, что ингридиентов может быть больше, чем помещается на экране, '
                            'используйте scroll', reply_markup=set_keyboard(SUPPER))

    elif message.text in COMPONENTS:
        answers.append(message.text)
        await message.reply('Отлично, выбор сделан!', reply_markup=types.ReplyKeyboardRemove())
        await message.reply(text=Waiter(user_id=message.from_user.id, answers=answers),
                            reply_markup=set_inlineKeyboard(inbuttons))


# Inline handler
@dp.callback_query_handler(text=inbuttons)
async def change_menu(callback):
    await callback.message.reply('Для какого приема пищи выбираем меню?',
                                 reply_markup=set_keyboard(['Завтрак', 'Ужин']))


# pre-checkout
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# Succesfull payment
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successfull_payment(message):
    print(message)
    await bot.send_message(message.chat.id, 'Поздравляю. Оплата прошла успешно. '
                                            'Теперь давайте пройдем авторизацию и начнем наш диалог \U0001F609',
                                            reply_markup=set_keyboard('Авторизация'))


# Running
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
