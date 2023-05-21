import asyncio
from aiogram import Bot, Dispatcher, executor, types
from ceredits import TOKEN_BOT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
import datetime

loop = asyncio.get_event_loop()
bot = Bot(TOKEN_BOT, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())


async def check(wait):
    while True:
        with open(f'users.js', 'r', encoding='UTF-8') as file:
            data = json.load(file)[0]
        print("check")
        for key, value in data.items():
            for key2, value2 in value.items():
                date_time = datetime.datetime.now()

                if len(value2["date"]) != 0:
                    date1, date2 = value2["date"][0], value2["date"][1]
                else:
                    date1, date2 = False, False


                time1, time2 = value2["time"][0], value2["time"][1]

                print(type(date_time.hour))
                if date1:
                    if date_time.month == int(date1) and date_time.day == int(date2) and date_time.hour == int(time1) and date_time.minute == int(time2) and not value2["viewed"]:
                        await bot.send_message(key, f"📣 {key2} 📣\n{value2['desc_logo']}\n")
                        value2["viewed"] = True
                        print(value2["viewed"])
                        with open(f'users.js', 'w', encoding='UTF-8') as file:
                            json.dump([data], file, indent=4, ensure_ascii=False)
                    elif (date_time.month != int(date1) or date_time.day != int(date2) or date_time.hour != int(time1) or date_time.minute != int(time2)) and value2["viewed"]:
                        value2["viewed"] = False
                        print(value2["viewed"])
                        with open(f'users.js', 'w', encoding='UTF-8') as file:
                            json.dump([data], file, indent=4,
                                      ensure_ascii=False)
                    else:
                        print("None")
                    
                else:
                    if date_time.hour == int(time1) and date_time.minute == int(time2) and not value2["viewed"]:
                        await bot.send_message(key, f"📣 {key2} 📣\n{value2['desc_logo']}\n")
                        value2["viewed"] = True
                        print(value2["viewed"])
                        with open(f'users.js', 'w', encoding='UTF-8') as file:
                            json.dump([data], file, indent=4, ensure_ascii=False)
                    elif (date_time.hour != int(time1) or date_time.minute != int(time2)) and value2["viewed"]:
                        value2["viewed"] = False
                        print(value2["viewed"])
                        with open(f'users.js', 'w', encoding='UTF-8') as file:
                            json.dump([data], file, indent=4,
                                      ensure_ascii=False)
                    else:
                        print("None")
                
        await asyncio.sleep(wait)

if __name__ == "__main__":
    dp.loop.create_task(check(10))
    from answer_main import dp, greetings_admin
    executor.start_polling(dp, on_startup=greetings_admin)
