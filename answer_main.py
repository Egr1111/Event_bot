from ceredits import TOKEN_BOT, ADMIN_ID
from datetime import datetime
import json
import logging
from main import bot, dp
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

from aiogram.dispatcher import FSMContext
from keyboard import choice
from newEvent import NewEvent
import datetime
import calendar
import locale

import random

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " "]
with open(f'users.js', 'r', encoding='UTF-8') as file:
    users = json.load(file)

all_users = users


async def greetings_admin(message=Message):

    if str(ADMIN_ID) not in all_users[0].keys():
        print(all_users[0].keys())
        all_users[0][f"{ADMIN_ID}"] = {}
        with open(f'users.js', 'w', encoding='UTF-8') as file:
            json.dump(all_users, file, indent=4, ensure_ascii=False)

    await bot.send_message(ADMIN_ID, text=f"Привет, дорогой админ!", reply_markup=choice)

@dp.callback_query_handler(lambda call: call.data == "/cancel")
async def main_answer(call_back = CallbackQuery):
    await bot.send_message(call_back.from_user.id, "Ну тогда выберите действие", reply_markup=choice)

@dp.message_handler(Command("start"))
async def greetings(message=Message):
    if f"{message.from_user.id}" not in all_users.keys():
        all_users[0][f"{message.from_user.id}"] = {}
        with open(f'users.js', 'w', encoding='UTF-8') as file:
            json.dump(all_users, file, indent=4, ensure_ascii=False)

    await message.answer(f"Привет, {message.from_user.first_name}! Я - бот-напоминалка и создан для того, чтобы напоминать людям об их делах. Выберите действие...", reply_markup=choice)


@dp.message_handler(text="🕒 Создать событие 🕒", state=None)
async def newEvent(message=Message):
    await message.answer("* - обязательно для заполнения, для того, чтобы заполнить пустоту, где это возможно, напишите 'none'")
    await message.answer("Чтобы отменить заполнение формы введите команду /cancel")
    await message.answer("Название события*")
    await NewEvent.logo.set()


@dp.message_handler(text="🔔 Мои события 🔔")
async def my_events(message=Message):
    events = all_users[0][f"{message.from_user.id}"]
    if len(events.keys()) != 0:
        await bot.send_message(message.from_user.id, "Ваши события:")
        cl = calendar
        strok = ""
        
        for i in range(len(events.keys())):
            event = events[list(events.keys())[i]]
            if event["date"] != []:
                if int(event["time"][1]) < 10:
                    strok += f"Событие {list(events.keys())[i]} запланировано на {cl.month_name[int(event['date'][0])]} {event['date'][1]} {event['time'][0]}:0{event['time'][1]}\n{event['desc_logo']}\n"
                else:
                    strok += f"Событие {list(events.keys())[i]} запланировано на {cl.month_name[int(event['date'][0])]} {event['date'][1]} {event['time'][0]}:{event['time'][1]}\n{event['desc_logo']}\n"
            else:
                if int(event["time"][1]) < 10:
                    strok += f"Событие {list(events.keys())[i]} запланировано на {event['time'][0]}:0{event['time'][1]}\n{event['desc_logo']}\n"
                else:
                    strok += f"Событие {list(events.keys())[i]} запланировано на {event['time'][0]}:{event['time'][1]}\n{event['desc_logo']}\n"

        await bot.send_message(message.from_user.id, strok, reply_markup=choice)
    else:
        await bot.send_message(message.from_user.id, "У вас нет событий", reply_markup=choice)


@dp.message_handler(text="🔕 Удалить событие 🔕")
async def delete_choice(message=Message):
    events = InlineKeyboardMarkup()
    if all_users[0][f"{message.from_user.id}"] != {}:
        for key, value in all_users[0][f"{message.from_user.id}"].items():
            events.add(InlineKeyboardButton(
                f"{key}", callback_data=f"/confirm {value['id']}"))
        events.add(InlineKeyboardButton(
            f"Отмена действия", callback_data=f"/cancel"))
        await message.answer("Выберите событие, которое Вы хотите удалить:", reply_markup=events)
    else:
        await message.answer("У вас нет событий.", reply_markup=choice)


@dp.callback_query_handler(lambda call: call.data == "🔕 Удалить событие 🔕")
async def delete_choice(call_back = CallbackQuery):
    events = InlineKeyboardMarkup()
    if all_users[0][f"{call_back.from_user.id}"] != {}:
        for key, value in all_users[0][f"{call_back.from_user.id}"].items():
            events.add(InlineKeyboardButton(
                f"{key}", callback_data=f"/confirm {value['id']}"))
        events.add(InlineKeyboardButton(
            f"Отмена действия", callback_data=f"/cancel"))
        await bot.send_message(call_back.from_user.id, "Выберите событие, которое Вы хотите удалить:", reply_markup=events)
    else:
        await bot.send_message(call_back.from_user.id, "У вас нет событий.", reply_markup=choice)


@dp.callback_query_handler(lambda call: "/confirm" in call.data.split(" ") and len(call.data.split(" ")) == 2)
async def delete_confirm(call_back=CallbackQuery):
    event = call_back.message['reply_markup']['inline_keyboard'][0][0]['callback_data'].split(" ")
    events = all_users[0][f"{call_back.from_user.id}"]
    count = 0
    for key, value in events.items():
        if value["id"] == event[1]:
            count += 1
            confirm = InlineKeyboardMarkup()
            cl = calendar
            await bot.send_message(call_back.from_user.id, "Вы действительно хотите удалить это событие?")
            confirm.add(InlineKeyboardButton(
                "Да", callback_data=f"/delete {value['id']}"))
            confirm.add(InlineKeyboardButton(
                "Нет", callback_data=f"🔕 Удалить событие 🔕"))

            if value["date"] != []:
                if int(value["time"][1]) < 10:
                    await bot.send_message(
                        call_back.from_user.id, f"Событие {key} запланировано на {cl.month_name[int(value['date'][0])]} {value['date'][1]} {value['time'][0]}:0{value['time'][1]}\n{value['desc_logo']}\n", reply_markup=confirm)
                else:
                    await bot.send_message(
                        call_back.from_user.id, f"Событие {key} запланировано на {cl.month_name[int(value['date'][0])]} {value['date'][1]} {value['time'][0]}:{value['time'][1]}\n{value['desc_logo']}\n", reply_markup=confirm)
            else:
                if int(value["time"][1]) < 10:
                    await bot.send_message(
                        call_back.from_user.id, f"Событие {key} запланировано на {value['time'][0]}:0{value['time'][1]}\n{value['desc_logo']}\n", reply_markup=confirm)
                else:
                    await bot.send_message(
                        call_back.from_user.id, f"Событие {key} запланировано на {value['time'][0]}:{value['time'][1]}\n{value['desc_logo']}\n", reply_markup=confirm)
    if count == 0:
        await bot.send_message(
            call_back.from_user.id, f"Этого события больше не существует", reply_markup=choice)


@dp.callback_query_handler(lambda call: "/delete" in call.data.split(" ") and len(call.data.split(" ")) == 2)
async def delete_confirm(call_back=CallbackQuery):
    event = call_back.message['reply_markup']['inline_keyboard'][0][0]['callback_data'].split(
        " ")
    new_dict = all_users[0][f"{call_back.from_user.id}"]
    print(new_dict)
    new_dict = {key: value for key,
                 value in new_dict.items() if value["id"] != event[1]}
    all_users[0][f"{call_back.from_user.id}"] = new_dict
    with open(f'users.js', 'w', encoding='UTF-8') as file:
        json.dump(all_users, file, indent=4, ensure_ascii=False)

    await bot.send_message(call_back.from_user.id, "Событие удалено", reply_markup=choice)


@dp.message_handler(text="🚫 Удалить все события 🚫")
async def destroy_choice(message = Message):
    if all_users[0][f"{message.from_user.id}"] != {}:
        last_choice = InlineKeyboardMarkup()
        last_choice.add(InlineKeyboardButton("Да", callback_data=f"/destroy"))
        last_choice.add(InlineKeyboardButton(
            "Нет", callback_data=f"/cancel"))
        await bot.send_message(message.from_user.id, "Вы уверены в этом?", reply_markup=last_choice)
    else:
        await bot.send_message(message.from_user.id, "У Вас нет событий", reply_markup=choice)

    

@dp.callback_query_handler(lambda call: call.data == "/destroy")
async def destroy_events(call_back = CallbackQuery):
    all_users[0][f"{call_back.from_user.id}"] = {}
    with open(f'users.js', 'w', encoding='UTF-8') as file:
        json.dump(all_users, file, indent=4, ensure_ascii=False)

    await bot.send_message(call_back.from_user.id, "Все имеющиеся события были стерты.", reply_markup=choice)
    
    


@dp.message_handler(state=NewEvent.logo)
async def logo(message=Message, state=FSMContext):
    if message.text != "/cancel":
        answer = message.text
        async with state.proxy() as data:
            data["logo"] = answer
        await message.answer("Описание события")

        await NewEvent.desc_logo.set()

    else:
        await state.reset_state(with_data=False)
        await message.answer("Создание события отменено", reply_markup=choice)


@dp.message_handler(state=NewEvent.desc_logo)
async def desc_logo(message=Message, state=FSMContext):
    if message.text != "/cancel" and message.text != "none":
        answer = message.text
        async with state.proxy() as data:
            data["desc_logo"] = answer
        await message.answer("Дата(месяц, день). Заполняте через пробел и только цифрами! Если вы напишите 'none', то данное событие будет проверяться каждый день, но если вы решите заполнить эту часть формы, то, пожалуста, заполняйте месяц и дату вместе во избежание ошибок.")
        await NewEvent.date.set()
    elif message.text == "none":
        async with state.proxy() as data:
            data["desc_logo"] = ""

        await message.answer("Дата(месяц, день). Заполняйте через пробел и только цифрами! Если вы напишите 'none', то данное событие будет проверяться каждый день, но если вы решите заполнить эту часть формы, то, пожалуста, заполняйте месяц и дату вместе во избежание ошибок.")
        await NewEvent.date.set()
    else:
        await state.reset_state(with_data=False)
        await message.answer("Создание события отменено", reply_markup=choice)


@dp.message_handler(state=NewEvent.date)
async def date(message=Message, state=FSMContext):
    count = 0
    if message.text != "/cancel" and message.text != "none":
        for i in message.text:
            if i not in num:
                await message.answer("Неправильно заполнена форма! Создание события отменено.", reply_markup=choice)
                await state.reset_state(with_data=False)
                count += 1
                break
        if count != 1:
            answer = message.text.split(" ")
            print(answer)
            while "" in answer:
                answer.remove("")
            for i in answer:
                print(i)
                
                if int(i) < 10 and len(i) > 1:
                    answer[answer.index(i)] = i.replace("0", "")
            print(answer)
            for i in answer:
                print(i, answer.index(i))
                if len(answer) == 1:
                    print(1)
                    await message.answer("Неправильно заполнена форма! Создание события отменено", reply_markup=choice)
                    await state.reset_state(with_data=False)
                    break
                if (len(i) > 2 or int(i) > 12 or int(i) < 1) and answer.index(i) == 0:
                    print(2)
                    await state.reset_state(with_data=False)
                    await message.answer("Не бывает " + i + " месяца! Создание события отменено", reply_markup=choice)
                    break

                elif (len(i) > 2 or int(i) > 31 or int(i) < 1) and answer.index(i) == 1:
                    print(3)
                    await state.reset_state(with_data=False)
                    await message.answer("Не бывает " + i + " дня! Создание события отменено", reply_markup=choice)
                    break
                elif answer.index(i) + 1 == len(answer):
                    print(4)
                    try:
                        date = datetime.datetime(
                            2021, int(answer[0]), int(answer[1]))
                        async with state.proxy() as data:
                            data["date"] = answer
                        await message.answer("Время(Час*, минута)")
                        print(4.1)
                        await NewEvent.time.set()
                    except:
                        print(4.2)
                        await state.reset_state(with_data=False)
                        await message.answer("Не бывает " + i + " дня в этом месяце! Создание события отменено", reply_markup=choice)

    elif message.text == "none":
        async with state.proxy() as data:
            data["date"] = []
            await message.answer("Время(Час*, минута)")
            await NewEvent.time.set()

    else:
        await state.reset_state(with_data=False)
        await message.answer("Создание события отменено", reply_markup=choice)


@dp.message_handler(state=NewEvent.time)
async def time(message=Message, state=FSMContext):
    count = 0
    if message.text != "/cancel" and message.text != "none":

        for i in message.text:
            if i not in num:
                await message.answer("Неправильно заполнена форма! Создание события отменено", reply_markup=choice)
                await state.reset_state(with_data=False)
                count += 1
                break
        if count != 1:
            answer = message.text.split(" ")
            print(answer)
            while "" in answer:
                answer.remove("")
            print(answer)
            for i in answer:
                if int(i) < 10 and len(i) > 1:
                    answer[answer.index(i)] = i.replace("0", "")
                elif int(i) < 10 and int(i) == 0:
                    answer[answer.index(i)] = "0"
            print(answer)

            for i in answer:
                if (len(i) > 2 or int(i) > 24 or int(i) < 1) and answer.index(i) == 0:
                    await state.reset_state(with_data=False)
                    await message.answer("Не бывает " + i + " часа! Создание события отменено", reply_markup=choice)
                    break

                elif (len(i) > 2 or int(i) > 59 or int(i) < 0) and answer.index(i) == 1:
                    await state.reset_state(with_data=False)
                    await message.answer("Не бывает " + i + " минуты! Создание события отменено", reply_markup=choice)
                    break

                elif answer.index(i) + 1 == len(answer) and len(answer) == 1:
                    async with state.proxy() as data:
                        data["time"] = [answer[0], "0"]
                    await message.answer("Событие создано", reply_markup=choice)
                    await NewEvent.time.set()

                    form = await state.get_data()
                    print(form)
                    id = random.randint(1, 1000000000000000000000000)
                    list_id = []
                    for key, value in all_users[0][f"{message.from_user.id}"].items():
                        if value != {}:
                            list_id.append(value["id"])
                    
                    while f"{id}" in list_id:
                        id = random.randint(1, 1000000000000000000000000)
                    all_users[0][f"{message.from_user.id}"][form["logo"]] = {
                        "desc_logo": form["desc_logo"],
                        "date": form["date"],
                        "time": form["time"],
                        "viewed": False,
                        "id": f"{id}"
                    }

                    with open(f'users.js', 'w', encoding='UTF-8') as file:
                        json.dump(all_users, file, indent=4,
                                  ensure_ascii=False)
                    await state.reset_state(with_data=False)

                elif answer.index(i) + 1 == len(answer) and len(answer) == 2:
                    async with state.proxy() as data:
                        data["time"] = answer
                    await message.answer("Событие создано", reply_markup=choice)
                    await NewEvent.time.set()

                    form = await state.get_data()
                    print(form)
                    id = random.randint(1, 1000000000000000000000000)
                    list_id = []
                    for key, value in all_users[0][f"{message.from_user.id}"].items():
                        if value != {}:
                            list_id.append(value["id"])

                    while f"{id}" in list_id:
                        id = random.randint(1, 1000000000000000000000000)
                    all_users[0][f"{message.from_user.id}"][form["logo"]] = {
                        "desc_logo": form["desc_logo"],
                        "date": form["date"],
                        "time": form["time"],
                        "viewed": False,
                        "id": f"{id}"
                    }

                    with open(f'users.js', 'w', encoding='UTF-8') as file:
                        json.dump(all_users, file, indent=4,
                                  ensure_ascii=False)
                    await state.reset_state(with_data=False)
    elif message.text == "none":
        async with state.proxy() as data:
            await message.answer("Должны быть хотя бы часы для успешного создания события. Создание события отменено", reply_markup=choice)
            await state.reset_state(with_data=False)
    else:
        await state.reset_state(with_data=False)
        await message.answer("Создание события отменено", reply_markup=choice)
