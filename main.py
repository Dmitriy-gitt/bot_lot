import telebot
import random
import schedule
import record
import write
import locale
import players
from datetime import datetime
from telebot import types  # для указание типов
import settings

token = settings.KEY
chatid = settings.CHAT_ID
bot = telebot.TeleBot(token)
text = {}
date = {}
password = settings.PASS
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

#Публикация поста о победителе, удаление даты розыгрыша из бд
def winner_post():
    c = record.connect()
    obj = c.all_select_date('data_lot')
    if obj is not None:
        for i in obj:
            my_dt = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            if my_dt < current_time:
                get_link = c.get_link(i)
                get_users = players.connect.select_users(get_link[0])
                print(get_users)
                winner = random.sample(list(get_users.keys()), int(get_link[-1]))
                get_photo_db = c.get_photo('data_lot', i)
                get_post_id = c.get_post_id(i)
                if int(get_link[-1]) > 1:
                    win = 'Победители'
                elif int(get_link[-1]) == 1:
                    win = 'Победитель'
                #Вывод поста о победителях в столбик с ссылкой на аккаунт
                caption = "\n🎉Результаты розыгрыша:\n{}:\n{}\n\n{}".format(win,"\n".join("{}. @<a href=\"tg://user?id={}\">{}</a>".format(winner.index(i)+1, i, get_users[i]) for i in winner), write.contact)
                bot.send_photo(chatid, get_photo_db, caption=caption, reply_to_message_id=get_post_id, parse_mode='html')
                #После определения победителя, убираем кнопку с поста о розыгрыше по id
                bot.edit_message_reply_markup(chatid, get_post_id, reply_markup=None)
                c.delete_date('data_lot', i)
        
#запуск функции, которая проверяет бд по времени
def func_time():
    schedule.every().day.at("18:20").do(deffered_post)
    schedule.every().day.at("18:22").do(winner_post)
    #schedule.every(1).minutes.do(deffered_post)
    #schedule.every(2).minutes.do(winner_post)
    print('ok')
    while True:
        schedule.run_pending()


#Проверка формата времени и вызов функции о публикации поста и о победителе
def deffered_post():
    global post_id
    c = record.connect()
    markup_participate = types.InlineKeyboardMarkup()
    participate = types.InlineKeyboardButton("Участвовать", callback_data="Участвовать")
    markup_participate.add(participate)
    
    obj = c.all_select_date('data_public')
    if obj is not None:
        for i in obj:
            my_dt = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            if my_dt < current_time:
                get_photo_db = c.get_photo('data_public', i)
                get_write = list(c.get_write(i))
                print(get_write, 'get_write')
                formatted_date = my_dt.strftime("%d %B в %H:%M")
                print(formatted_date)
                post = bot.send_photo(chatid, get_photo_db, caption=f'{get_write[0]}\n\n{write.text_post}\n\nИтоги подведём {formatted_date} при помощи бота, он случайно выбирает победителя.\nВсем удачи 🤞🏼', reply_markup=markup_participate) #\nДата розыгрыша:\n{c.get_write(i)[1]
                get_write.clear()
                post_id = post.id
                post_link = f'https://t.me/testtestaz/{post.id}'
                #добавляем id поста в бд
                c.add_post_id(post_id, i)
                c.add_link(post_link, i)
                c.delete_date('data_public' ,i)


#Приветствие пользователя и выбор команд
@bot.message_handler(commands=[f'start{password}', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    menu = types.InlineKeyboardButton("Список розыгрышей", callback_data="Список")
    new_lot = types.InlineKeyboardButton("Создать розыгрыш", callback_data="Создать")
    markup.add(menu, new_lot)
    if message.text == f'/start{password}':
        bot.send_message(message.chat.id, f"Приветсвуем вас, <b>{message.from_user.first_name}</b>\n" 
        "для создания розыгрыша напишите текст для поста", reply_markup=markup, parse_mode="HTML")
        print(datetime.now())
        func_time()
    elif message.text == '/menu':
        bot.send_message(message.chat.id, f"Вы вернулись в меню", reply_markup=markup)


#Получение фото от пользователя
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    global photo_chat
    markup = types.InlineKeyboardMarkup()
    post = types.InlineKeyboardButton("Показать пост", callback_data="Показать пост")
    markup.add(post)
    bot.send_message(message.chat.id, text="Фото для поста загружено, \nПоказать пост?", reply_markup=markup)
    #получить фото по id
    photo_chat = message.photo[-1].file_id


#Обработка кнопок InlineKeyboardButton
@bot.callback_query_handler(func=lambda callback: True)
def handle_button_click(callback):
    c = record.connect()
    #Показать список розыгрышей
    if callback.data == 'Список':
        all_link = c.get_all_link()
        print(all_link)
        n = '\n'
        if all_link is not None and len(all_link)>0:
            bot.send_message(callback.message.chat.id, 'Список постов\n{}'.format('\n'.join(' - '.join([i[0], i[1][:20]]) for i in all_link)))
        else:
            bot.send_message(callback.message.chat.id, 'Список пуст')
        """ all_link = c.get_all_link()
        print(all_link)
        n = '\n'
        if all_link is not None and len(all_link)>0:
            bot.send_message(callback.message.chat.id, f'Список постов\n{f"{n}".join(' - '.join([i[0], i[1][:20]]) for i in all_link)}')
        else:
            bot.send_message(callback.message.chat.id, 'Список пуст') """
    elif callback.data == 'Создать':
        msg = bot.send_message(callback.message.chat.id, 'Введите текст для поста')
        bot.register_next_step_handler(msg, save_text)
    elif callback.data == 'Показать пост':
        select_table = list(c.select_table())
        print(select_table)
        my_dt = datetime.strptime(select_table[0][2], '%Y-%m-%d %H:%M:%S')
        formatted_date = my_dt.strftime("%d %B в %H:%M")
        print(formatted_date, select_table[0][2])
        bot.send_photo(callback.message.chat.id, photo_chat, caption=f"{select_table[0][2]}\n\n{write.text_post}\n\nИтоги подведём {formatted_date} при помощи бота, он случайно выбирает победителя.\nВсем удачи 🤞🏼"
                       f"\n---------------\nДата розыгрыша:\n{select_table[0][2]}")
        mes = bot.send_message(callback.message.chat.id, f'Укажите дату публикации в формате\n2023-01-12 12:00:00\n{write.gmt}')
        #добавляем фото по id и дате розыгрыша в бд
        c.add_photo(photo_chat, select_table[0][2])
        print(select_table, 'selec_table')
        select_table.clear()
        bot.register_next_step_handler(mes, publish_by_time)
    elif callback.data == 'Опубликовать':
        bot.send_message(callback.message.chat.id, f'Пост опубликуется в {c.select_date()}')
    elif callback.data == 'Участвовать':
        link = f'https://t.me/testtestaz/{callback.message.message_id}'
        id = callback.from_user.id
        all_users = list(players.connect.select_users(link).values())
        if callback.from_user.first_name in all_users or  callback.from_user.username in all_users:
            bot.answer_callback_query(callback.id, show_alert=True, text=f"Вы уже участвуете в розыгрыше\nУчастников: {len(all_users)}")
        else:
            #Проверка, подписан ли человек на канал и забираем username, если есть, если нет, то получаем  имя без @ссылки на человека    
            member = bot.get_chat_member(chatid, id)
            if member.status == 'member' or member.status == 'creator' and member.status != 'bot':
                    if callback.from_user.username != None:
                        #добавляем участника и ссылку в бд
                        players.connect.add_player(id, callback.from_user.username, link)
                        bot.answer_callback_query(callback.id, show_alert=True, text=f"Вы участвуете в розыгрыше\nУчастников: {len(all_users)+1}")
                    elif callback.from_user.username == None:
                        #добавляем участника и ссылку в бд
                        players.connect.add_player(id, callback.from_user.first_name, link)
                        bot.answer_callback_query(callback.id, show_alert=True, text=f"Вы участвуете в розыгрыше\nУчастников: {len(all_users)+1}")
            else:
                bot.answer_callback_query(callback.id, show_alert=True, text="Для участия, подпишитесь на канал")

#Получение и сохранение текста
def save_text(callback):
    global user_id
    user_id = callback.from_user.id
    text[user_id] = callback.text
    mes = bot.send_message(callback.chat.id, f'Текст сохранен \nВведите дату розыгрыша в формате \n2023-01-12 12:00:00\n{write.gmt}')
    bot.register_next_step_handler(mes, date_lottery)

#Получаем дату розыгрыша
def date_lottery(callback):
    global date_lottery_string
    date_lottery_string = callback.text
    date_format = '%Y-%m-%d %H:%M:%S'
        #проверка на формат даты
    try:
        datetime.strptime(date_lottery_string, date_format)
        date_post = callback.from_user.id
        date[date_lottery_string] = date_lottery_string
        mes = bot.send_message(callback.chat.id, 'Дата сохранена\nУкажите количество победителей')
        bot.register_next_step_handler(mes, number_winners)

    #здесь просим ввести дату корректно, вызываем эту же функцию(рекурсия)
    except ValueError:
        bot.send_message(callback.chat.id, f'Формат даты неверный, попробуйте еще раз, формат даты\n2023-01-12 12:00:00\n{write.gmt}')
        bot.register_next_step_handler(callback, date_lottery)

#Получаем дату публикации поста
def publish_by_time(mes):
    global date_string
    c = record.connect()
    markup = types.InlineKeyboardMarkup()
    publish = types.InlineKeyboardButton("Опубликовать пост", callback_data="Опубликовать")
    markup.add(publish)
    date_string = mes.text
    date_format = '%Y-%m-%d %H:%M:%S'
    # проверка на формат даты
    try:
        datetime.strptime(date_string, date_format)
        date[date_string] = date_string
        bot.send_message(mes.chat.id, 'Дата сохранена\n'
            'Опубликовать пост в указаную дату в канале https://t.me/testtestaz ?', reply_markup=markup)
        #вызов функции для добавления текста, даты публикации, даты розыгрыша
        c.add_date(date[date_string])

    # здесь просим ввести дату корректно, вызываем эту же функцию(рекурсия)
    except ValueError:
        bot.send_message(mes.chat.id, f'Формат даты неверный, попробуйте еще раз, формат даты\n2023-01-12 12:00:00\n{write.gmt}')
        bot.register_next_step_handler(mes, publish_by_time)

#Получаем кол-во победителей и отправляем текст, дату розыгрыша, кол-во победителей в бд
def number_winners(mes):
    global number
    c = record.connect()
    number = mes.text
    bot.send_message(mes.chat.id, 'Количество победителей сохранено, загрузите фото')
    c.add_table(text[user_id], date[date_lottery_string], number)



bot.polling(none_stop=True)