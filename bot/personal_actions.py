from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotDB

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db_result=BotDB.check_user_exists(message.from_user.id);
    if (db_result is None):
        await message.bot.send_message(message.from_user.id, BotDB.get_message("start_hello_message"))
    else:
        await message.bot.send_message(message.from_user.id,  BotDB.get_message("start_hello_messageFor") % (str(db_result[0])))
        if (db_result[5] == 0):
            await message.bot.send_message(message.from_user.id, BotDB.get_message("start_confirmReg_message"))
        if (db_result[5] == 2):
            await message.bot.send_message(message.from_user.id, BotDB.get_message("start_ban_message"))
        if (db_result[5] == 1):
            await message.bot.send_message(message.from_user.id, BotDB.get_message("start_regIsConfirmed_message"))

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.bot.send_message( message.chat.id, BotDB.get_message("help_message"))

@dp.message_handler()
async def echo_message(message: types.Message):
    db_result=BotDB.check_user_exists(message.from_user.id);
    if (db_result is None):
        # новый пользователь: проверка сообщения на формат фио и т п.
        user_data = message.text
        user_data = user_data.strip().split(",")
        
        if (len(user_data) == 3): # параметров должно быть 3
            phone=check_phone(str(user_data[1]).strip()) # проверка номера телефона
            if(phone is None):
                await message.bot.send_message(message.chat.id, BotDB.get_message("error_checkPhone_message"))
            else:
                num=str(user_data[2]).strip() # проверка номера участка
                if (not num.isnumeric()):
                    await message.bot.send_message(message.chat.id, BotDB.get_message("error_checkSector_message"))
                else:
                    uname=str(user_data[0]).strip() # проверка ФИО
                    if(not re.match(r"^(?=.{1,40}$)[а-яёА-ЯЁ]+(?:[-' ][а-яёА-ЯЁ]+)*$", uname)):
                        await message.bot.send_message(message.chat.id, BotDB.get_message("error_checkName_message"))
                    else:
                        if (BotDB.add_user( uname, phone, num, message.from_user.id)): # записываем результат в базу
                            await message.bot.send_message(message.chat.id, BotDB.get_message("regIsCompleted_message") % (uname, phone, num))
                        else:
                            await message.bot.send_message(message.chat.id, BotDB.get_message("error_reg_message"))

        # параметров меньше - пусть вводят заного
        else:
            await message.bot.send_message(message.from_user.id, BotDB.get_message("error_repeatReg_message"))
    else:
        if (db_result[5] == 0): # ожидает регистрации
            await message.bot.send_message(message.from_user.id, BotDB.get_message("start_confirmReg_message"))
        if (db_result[5] == 2): # бан
            await message.bot.send_message(message.from_user.id, BotDB.get_message("start_ban_message"))
        if (db_result[5] == 1): # заявки
            # пользователь существует и авторизован, значит ввёл заявку. проверяем правильность заполнения
            user_req = message.text
            user_req = user_req.strip().split(" ")
        
            if (len(user_req) == 2): # параметров должно быть 2
                a_num = user_req[0].strip()
                a_model = user_req[1].strip()
                if (not re.match(r'^\w?(\d{3})(\w{2}(\d{2,3})?)?', a_num)):
                    await message.bot.send_message(message.from_user.id, BotDB.get_message("error_checkCarNum_message"))
                else:
                    await message.bot.send_message(message.from_user.id, BotDB.get_message("requestIsCompleted_message") % (a_num, a_model))
            else:
                # заявка заполнена не правильно - предупреждение
                await message.bot.send_message(message.from_user.id, BotDB.get_message("error_repeatRequest"))


def check_phone( text ):
    if(not re.match(r'^((8|\+7)[\- ]?)(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', text)):
        return None
    else:
        list1 = re.findall(r'\d', text)
        list1 = ''.join(list1)
        if len(list1) == 10:
            result = re.sub(r'(\d{3})(\d{3})(\d{2})(\d{2})', r'+7 \1 \2-\3-\4', list1)
        else:
            result = re.sub(r'(\d)(\d{3})(\d{3})(\d{2})(\d{2})', r'+7 \2 \3-\4-\5', list1)
        return result
