import telebot
from telebot import types

# Создаем экземпляр бота
API_TOKEN = 'YOU_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Определяем список товаров
products = [
    {
        "name": "Смартфон",
        "description": "Высокопроизводительный смартфон с большим экраном и отличной камерой."
    },
    {
        "name": "Ноутбук",
        "description": "Портативный и мощный ноутбук для работы и развлечений."
    },
    {
        "name": "Наушники",
        "description": "Беспроводные наушники с шумоподавлением и длительным временем работы."
    }
]

# Список админов
admins = [ID_ADMINS]
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text="Добро пожаловать в каталог товаров!")
    show_product(message.chat.id, 0)

# Функция для отображения товара
def show_product(chat_id, index):
    if index < len(products):
        product = products[index]
        keyboard = types.InlineKeyboardMarkup()
        heart_button = types.InlineKeyboardButton("❤️", callback_data=f"heart_{index}")
        dislike_button = types.InlineKeyboardButton("👎", callback_data=f"dislike_{index}")
        keyboard.add(heart_button, dislike_button)
        bot.send_message(chat_id=chat_id, text=product["name"], reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id, text="Каталог товаров закончился. Спасибо за просмотр!")

# Обработчик нажатия на кнопки
@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    data = call.data.split("_")
    action = data[0]
    index = int(data[1])

    if action == "heart":
        product = products[index]
        bot.send_message(call.message.chat.id, text=product["description"])
    elif action == "dislike":
        show_product(call.message.chat.id, index + 1)

# Обработчик команды /add для админов
@bot.message_handler(commands=['add'])
def add_product(message):
    if message.chat.id in admins:
        bot.send_message(chat_id=message.chat.id, text="Введите название нового товара:")
        bot.register_next_step_handler(message, get_product_name)
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав для добавления товаров.")

# Функция для получения названия товара
def get_product_name(message):
    name = message.text
    bot.send_message(chat_id=message.chat.id, text="Введите описание товара:")
    bot.register_next_step_handler(message, get_product_description, name)

# Функция для получения описания товара
def get_product_description(message, name):
    description = message.text
    new_product = {"name": name, "description": description}
    products.append(new_product)
    bot.send_message(chat_id=message.chat.id, text="Товар успешно добавлен!")

# Запуск бота
bot.polling()