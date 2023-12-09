import csv
import os
import random
import time

import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет, ты написал мне /start или /help.\n"
                                      "Введи /users, чтобы посмотреть инфформацию о пользователе\nМои пользователи: /my_users.")

@bot.message_handler(commands=['users'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/users/{random.randint(1, 10)}"
    response = requests.get(url)
    if response.status_code == 200:
        users = response.json()
        idx = users['id']
        name = users['name']
        username = users['username']
        email = users['email']
        street = users['address']['street']
        suite = users['address']['suite']
        city = users['address']['city']
        zipcode = users['address']['zipcode']
        lat = users['address']['geo']['lat']
        lng = users['address']['geo']['lng']
        phone = users['phone']
        website = users['website']
        namec = users['company']['name']
        catchPhrase = users['company']['catchPhrase']
        bs = users['company']['bs']

        telegram_user_id = message.from_user.id

        bot.send_message(message.chat.id, f"Имя: {users['name']}\nИмя пользователя: {users['username']}\nEmail: {users['email']}\nАдрес:\nДом: {users['address']['suite']}\nГород: {users['address']['city']}\nПочтовый индекс: {users['address']['zipcode']}\nГеолокация:\nШирота: {users['address']['geo']['lat']}"
                                          f"\nДолгота: {users['address']['geo']['lng']}\nТелефон: {users['phone']}\nВеб-сайт: {users['website']}\nКомпания:\nНазвание: {users['company']['name']}\nКоронная фраза: {users['company']['catchPhrase']}\nБанковская подписка: {users['company']['bs']}")
        with open(f'users_{telegram_user_id}.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Имя', 'Имя пользователя', 'Email', 'Адрес', 'Улица', 'Дом', 'Город', 'Почтовый индекс',
                          'Геолокация', 'Широта', 'Долгота', 'Телефон', 'Веб-сайт', 'Название', 'Коронная фраза', 'Банковская подписка', 'Время']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            named_tuple = time.localtime()
            time_string = time.strftime("%d/%m/%Y, %H:%M", named_tuple)
            writer.writerow({
                'id': idx,
                'Имя': name,
                'Имя пользователя': username,
                'Email': email,
                'Улица': street,
                'Дом': suite,
                'Город': city,
                'Почтовый индекс': zipcode,
                'Широта': lat,
                'Долгота': lng,
                'Телефон': phone,
                'Веб-сайт': website,
                'Название': namec,
                'Коронная фраза': catchPhrase,
                'Банковская подписка': bs,
                'Время': time_string,

            })
    else:
        bot.send_message(message.chat.id, "Данные не найдены")

@bot.message_handler(commands=['my_users'])
def handle_my_todos(message):
    user_id = message.from_user.id
    try:
        with open(f'users_{user_id}.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bot.send_message(message.chat.id,
                                 f"ID: {row['id']}\n"
                                 f"Имя: {row['Имя']}\n"
                                 f"Имя пользователя: {row['Имя пользователя']}\n"
                                 f"Email: {row['Email']}\n"
                                 f"Улица: {row['Улица']}\n"
                                 f"Дом: {row['Дом']}\n"
                                 f"Город: {row['Город']}\n"
                                 f"Почтовый индекс: {row['Почтовый индекс']}\n"
                                 f"Широта: {row['Широта']}\n"
                                 f"Долгота: {row['Долгота']}\n"
                                 f"Телефон: {row['Телефон']}\n"
                                 f"Веб-сайт: {row['Веб-сайт']}\n"
                                 f"Название: {row['Название']}\n"
                                 f"Коронная фраза: {row['Коронная фраза']}\n"
                                 f"Банковская подписка: {row['Банковская подписка']}\n"
                                 f"Время: {row['Время']}"
                                 )

    except FileNotFoundError:
        bot.send_message(message.chat.id, "У вас нет сохраненных постов.")

bot.polling(none_stop=True)
