
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup
from commands import biglion_api_city, biglion_api_category, biglion_api_link

storage = MemoryStorage()
bot = Bot(TOKEN)  # указываем Token для бота
dp = Dispatcher(bot, storage=storage)

url = "C:\\Users\\User\\miniconda3yyyyy\\biglion\\"  # Корневой каталог с картинками

help = '''
1) Вызовите команду /city
2) Выберете город
3) Выберете нужную категорию  из меню
4) Выберите нужную акцию и перейдите на сайт или в приложение Biglion'''


class UserState(StatesGroup):
    city = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, я бот Biglion. Я помогу тебе найти акции в твоём городе')
    await message.answer(help)


@dp.message_handler(commands=['city'])
async def city(message: types.Message):

    markup = types.InlineKeyboardMarkup()
    for city_name in biglion_api_city():
        markup.add(types.InlineKeyboardButton(str(city_name), callback_data=str(city_name)))
    await message.answer('Выбери город из меню', reply_markup=markup)


@dp.callback_query_handler()
async def callback(call, state: FSMContext):
    await state.update_data(city=call.data)
    if call.data:
        markup = types.ReplyKeyboardMarkup()
        for category_name in biglion_api_category():
            markup.add(types.KeyboardButton(str(category_name)))
        markup.add(types.KeyboardButton('Изменить город'))
        await call.message.answer('Выбери категорию из меню', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def link_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text in biglion_api_category():
        for link_name in biglion_api_link(data['city'], message.text):
            markup = types.InlineKeyboardMarkup()
            await message.answer(biglion_api_link(data['city'], message.text)[link_name][1]) # Выводим название акции
            markup.add(types.InlineKeyboardButton('Смотреть на сайте или в приложении', url=link_name))
            file = open(url + biglion_api_link(data['city'], message.text)[link_name][0], 'rb')  # Открываем картинку
            await bot.send_photo(chat_id=message.chat.id, photo=file, reply_markup=markup)

    elif message.text == 'Изменить город':
        await message.answer('/city')
        await state.finish()

    else:
        await message.answer('Неверная команда')
        await message.answer(help)
        await state.finish()


executor.start_polling(dp)



