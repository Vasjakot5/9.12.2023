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
                                      "Используй /todos для получения рандомной цитаты, /comments для получения рандомного комментария или /posts для получения рандомного поста.\nМои задачи: /my_todos\n"
                                      "Мои комментарии: /my_comments\n""Мои посты: /my_posts")

@bot.message_handler(commands=['posts'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/posts/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json()
        idx = posts['id']
        title = posts['title']
        body = posts['body']

        telegram_user_id = message.from_user.id

        bot.send_message(message.chat.id, f"Заголовок: {posts['title']}\nТекст: {posts['body']}")
        with open(f'posts_{telegram_user_id}.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Заголовок', 'Текст', 'Время']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            named_tuple = time.localtime()
            time_string = time.strftime("%d/%m/%Y, %H:%M", named_tuple)
            writer.writerow({
                'id': idx,
                'Заголовок': title,
                'Текст': body,
                'Время': time_string,
            })
    else:
        bot.send_message(message.chat.id, "Данные не найдены")

@bot.message_handler(commands=['my_posts'])
def handle_my_todos(message):
    user_id = message.from_user.id
    try:
        with open(f'posts_{user_id}.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bot.send_message(message.chat.id,
                                 f"ID: {row['id']}\n"
                                 f"Заголовок: {row['Заголовок']}\n"
                                 f"Текст: {row['Текст']}"
                                 )

    except FileNotFoundError:
        bot.send_message(message.chat.id, "У вас нет сохраненных постов.")


@bot.message_handler(commands=['comments'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/comments/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        comments = response.json()
        idx = comments['id']
        name = comments['name']
        email = comments['email']
        body = comments['body']

        telegram_user_id = message.from_user.id

        bot.send_message(message.chat.id, f"Имя: {comments['name']}\nEmail: {comments['email']}\nТекст: {comments['body']}")
        with open(f'comments_{telegram_user_id}.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Имя', 'Email', 'Текст', 'Время']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            named_tuple = time.localtime()
            time_string = time.strftime("%d/%m/%Y, %H:%M", named_tuple)
            writer.writerow({
                'id': idx,
                'Имя': name,
                'Email': email,
                'Текст': body,
                'Время': time_string,
            })
    else:
        bot.send_message(message.chat.id, "Данные не найдены")

@bot.message_handler(commands=['my_comments'])
def handle_my_todos(message):
    user_id = message.from_user.id
    try:
        with open(f'comments_{user_id}.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bot.send_message(message.chat.id,
                                 f"ID: {row['id']}\n"
                                 f"Имя: {row['Имя']}\n"  
                                 f"Email: {row['Email']}\n"
                                 f"Текст: {row['Текст']}"
                                 )

    except FileNotFoundError:
        bot.send_message(message.chat.id, "У вас нет сохраненных комментариев.")

@bot.message_handler(commands=['todos'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/todos/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        todos = response.json()
        idx = todos['id']
        title = todos['title']
        userid = todos['userId']

        telegram_user_id = message.from_user.id

        if bool(todos['completed']):
            completed = 'Выполнено'
        else:
            completed = 'Не выполнено'
        bot.send_message(message.chat.id, f"Задача: {todos['title']}\nСтатус: {completed}")
        with open(f'todos_{telegram_user_id}.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Заголовок', 'Пользователь', 'Статус', 'Время']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            named_tuple = time.localtime()
            time_string = time.strftime("%d/%m/%Y, %H:%M", named_tuple)
            writer.writerow({
                'id': idx,
                'Заголовок': title,
                'Пользователь': userid,
                'Статус': completed,
                'Время': time_string,
            })
    else:
        bot.send_message(message.chat.id, "Задача не найдена")

@bot.message_handler(commands=['my_todos'])
def handle_my_todos(message):
    user_id = message.from_user.id
    try:
        with open(f'todos_{user_id}.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                bot.send_message(message.chat.id,
                                 f"ID: {row['id']}\n"
                                 f"Заголовок: {row['Заголовок']}\n"
                                 f"Пользователь: {row['Пользователь']}\n"
                                 f"Статус: {row['Статус']}"
                                 )

    except FileNotFoundError:
        bot.send_message(message.chat.id, "У вас нет сохраненных задач.")

bot.polling(none_stop=True)
