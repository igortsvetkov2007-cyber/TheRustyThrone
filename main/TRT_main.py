from aiogram import Bot,Dispatcher,F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message,KeyboardButton,FSInputFile,LabeledPrice,PreCheckoutQuery
import asyncio
from threading import Thread
import time
import random
from datetime import datetime
from TRT_info import *

bot=Bot(BOT_TOKEN)
dp=Dispatcher()

units_count_dict={}
war_school_count_dict={}
medics_school_count_dict={}
units_define_dict={}
units_attack_dict={}
medics_attack_dict={}
units_attack_flags=[]
gold_count_dict={}
users_buy_dict={}

admin_flag=None
admin_message_flag=None

async def main():
    Thread(target=units_count).start()
    await dp.start_polling(bot)

async def account_check(message):
    cursor.execute('select login from Users where chat_id=?',(message.chat.id,))
    info_account=cursor.fetchall()    
    if info_account==[]:
        await bot.send_message(chat_id=message.chat.id,text='Не смогли обнаружить ваш аккаунт!')
        await bot.send_message(chat_id=message.chat.id,text='Игра начинается заново!')
        await bot_start(message)
    else:
        if info_account[0][0]==None:
            cursor.execute('delete from Users where chat_id=?',(message.chat.id,))
            await bot.send_message(chat_id=message.chat.id,text='Не смогли обнаружить ваш аккаунт!')
            await bot.send_message(chat_id=message.chat.id,text='Игра начинается заново!')
            await bot_start(message)
    connection.commit()

def units_count():
    while True:
        time.sleep(3600)
        for key in list(units_count_dict.keys()):
            units_count_dict[key]+=random.randint(1,5)
        for key in list(gold_count_dict.keys()):
            gold_count_dict[key]+=1
        for key in list(war_school_count_dict.keys()):
            war_school_count_dict[key]+=1
        for key in list(medics_school_count_dict.keys()):
            medics_school_count_dict[key]+=1

async def units_collect(message):
    if message.chat.id not in list(units_count_dict.keys()):
        units_count_dict[message.chat.id]=0
    if message.chat.id not in list(war_school_count_dict.keys()):
        war_school_count_dict[message.chat.id]=0
    if message.chat.id not in list(medics_school_count_dict.keys()):
        medics_school_count_dict[message.chat.id]=0
    if units_count_dict[message.chat.id]>0:
        cursor.execute('update Users set units_passive_number=units_passive_number+? where chat_id=?',(units_count_dict[message.chat.id],message.chat.id))
        connection.commit()
        await bot.send_message(chat_id=message.chat.id,text=f'С Гнилых Земель к вам прибыло {units_count_dict[message.chat.id]} добровольцев! Они хотят воевать за вас!')
        units_count_dict[message.chat.id]=0
        
async def xp_count(message):
    if message.chat.id not in list(units_count_dict.keys()):
        units_count_dict[message.chat.id]=0
    if message.chat.id not in list(war_school_count_dict.keys()):
        war_school_count_dict[message.chat.id]=0
    if message.chat.id not in list(medics_school_count_dict.keys()):
        medics_school_count_dict[message.chat.id]=0
    cursor.execute('select xp,level from Users where chat_id=?',(message.chat.id,))
    info_level=cursor.fetchall()[0]
    if info_level[1]==len(xp_levels)+1:
        cursor.execute('update Users set xp=0 where chat_id=?',(message.chat.id,))
        connection.commit()
    elif info_level[0]<=0:
        await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка повышения уровня.png'),caption=f'НОВЫЙ УРОВЕНЬ!!!!\nУРОВЕНЬ КОМАНДИРА ПОВЫШЕН ДО {info_level[1]+1}!!!!')
        if info_level[1]==len(xp_levels):
            time.sleep(2)
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка максимального уровня.png'),caption='ПОЗДРАВЛЯЕМ ВАС!!!!\nВЫ ДОСТИГЛИ МАКСИМАЛЬНОГО УРОВНЯ!!!!')
            cursor.execute('update Users set level=level+1,xp=? where chat_id=?',(0,message.chat.id))
            connection.commit()
            return
        cursor.execute('update Users set level=level+1,xp=? where chat_id=?',(xp_levels[info_level[1]]+1,message.chat.id))
        connection.commit()

@dp.message(Command('start'))
async def bot_start(message):
    keyboard=builder_start.as_markup(resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/вступительная картинка.png'),caption='Мир разрушен, а цивилизация на грани гибели! Люди поделились на миниатюрные государства со своими лидерами. До начала глобальной войны вы были известны, как талантливый и опытный главнокомандующий! На Гнилых Землях вы нашли полузаброшенную военную базу, и люди, находившиеся там, лишённые предводителя и погружённые в отчаяние, с радостью приняли вас в качастве нового командира!')
    await bot.send_message(chat_id=message.chat.id,text='Вы готовы взять ответственность за свой народ?',reply_markup=keyboard)
    cursor.execute('select units_active_number from Users where chat_id=?',(message.chat.id,))
    info_units=cursor.fetchall()
    if info_units==[]:
        cursor.execute('update Users set units_active_number=0 where chat_id=?',(message.chat.id,))
        connection.commit()

@dp.message(F.text=='ПЕРЕЗАПУСТИТЬ БОТА')
async def bot_reload(message):
    if message.chat.id in units_count_dict.keys():
        units_count_dict.pop(message.chat.id)
    if message.chat.id in gold_count_dict.keys():
        gold_count_dict.pop(message.chat.id)
    if message.chat.id in war_school_count_dict.keys():
        war_school_count_dict.pop(message.chat.id)
    if message.chat.id in medics_school_count_dict.keys():
        medics_school_count_dict.pop(message.chat.id)
    await bot_start(message)

@dp.message(F.text=='⚔ДА! Я ГОТОВ!⚔')
async def ready_button_func(message):
    cursor.execute('select * from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()
    if info==[]:
        cursor.execute('''insert into Users(chat_id,level,xp,rating,gold,gold_level,defense_level,tank_level,units_passive_number,units_active_number,units_defense_restriction,
                       units_attack_restriction,war_school_level,medics_school_level,heal_auto_level,medics_passive_number,medics_attack_restriction)
                       values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (message.chat.id,0,10,0,50,0,1,1,100,0,10,10,0,0,0,15,0))
        connection.commit()
        units_count_dict[message.chat.id]=0
        gold_count_dict[message.chat.id]=0
    keyboard=builder_begin_game.as_markup(resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка определения аккаунта.png'),caption='На этой глобальной войне вам предстоит руководить войсками, распределять ресурсы клана и стать Императором Ржавого Трона!',reply_markup=keyboard)    

@dp.message(F.text=='⚔️ВПЕРЁД!⚔️')
async def begin_game_button_func(message):
    cursor.execute('select login from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()    
    if info[0][0]==None:
        await bot.send_message(chat_id=message.chat.id,text='Как нам называть своего командира?')
    else:
        cursor.execute('select login from Users where chat_id=?',(message.chat.id,))
        info=cursor.fetchall()
        keyboard=builder_main_menu.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Добро пожаловать в крепость, {info[0][0]}',reply_markup=keyboard)

@dp.message(F.text=='⚔️ИНФОРМАЦИЯ⚔️')
async def army_info_func(message):
    if message.chat.id not in list(units_count_dict.keys()):
        units_count_dict[message.chat.id]=0
    if message.chat.id not in list(war_school_count_dict.keys()):
        war_school_count_dict[message.chat.id]=0
    if message.chat.id not in list(medics_school_count_dict.keys()):
        medics_school_count_dict[message.chat.id]=0
    await units_collect(message)
    cursor.execute('''select units_passive_number,units_active_number,gold,gold_level,defense_level,tank_level,level,xp,
                      war_school_level,medics_school_level,medics_passive_number,heal_auto_level from Users where chat_id=?''',(message.chat.id,))
    info=cursor.fetchall()
    level_string=''
    if info[0][6]==20:
        level_string='максимальный'
    else:
        level_string=str(info[0][7])+'XP до следующего уровня'
    await bot.send_message(chat_id=message.chat.id,text=f'''Приказ по сбору статистики выполнен!
Уровень командира {info[0][6]} ({level_string})
В резерве воинов: {info[0][0]}🪖
В резерве медиков: {info[0][10]}🏥
На оборонительных рубежах воинов: {info[0][1]}🪖
Золотых монет: {info[0][2]}🪙
Золотая шахта {info[0][3]} уровня, приносящая {gold_levels[info[0][3]]}🪙 в час
Военная школа {info[0][8]} уровня, выпускающая {war_school_levels[info[0][8]]}🪖 в час
Медицинская школа {info[0][9]} уровня, выпускающая {medics_school_levels[info[0][9]]}🏥 в час
Оборонительный рубеж {info[0][4]} уровня для размещения {defense_levels[info[0][4]-1]}🪖
Бронетранспортёр {info[0][5]} уровня, вмещающий {tank_levels[info[0][5]-1]}🪖
Медицинский автомобиль {info[0][11]} уровня, вмещающий {heal_auto_levels[info[0][11]]}🏥''')

@dp.message(F.text=='⚔️РАСПРЕДЕЛЕНИЕ ВОЙСК⚔️')
async def army_define_func(message):
    await bot_start(message)
    keyboard=builder_units_define.as_markup(resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка распределения войск.png'),caption='Войска ждут вашего приказа, командир!',reply_markup=keyboard)
    
@dp.message(F.text=='⚔️НАЗНАЧИТЬ ВОЙСКА ИЗ РЕЗЕРВА⚔️')
async def units_active_direct(message):
    await bot_start(message)
    cursor.execute('select units_active_number,units_defense_restriction,units_passive_number from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас на оборонительных рубежах находятся {info[0][0]} воинов (максимум {info[0][1]}), в резерве {info[0][2]} воинов')
    await bot.send_message(chat_id=message.chat.id,text='Назначте колличество воинов, которые отправятся из резерва в оборону или введите "!", чтобы заполнить рубежи до максимума.')
    units_define_dict[message.chat.id]='active'

@dp.message(F.text=='⚔️ОТОЗВАТЬ ВОЙСКА В РЕЗЕРВ⚔️')
async def units_passive_direct(message):
    cursor.execute('select units_active_number,units_passive_number from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас на оборонительных рубежах находятся {info[0][0]} воинов, в резерве {info[0][1]}')
    await bot.send_message(chat_id=message.chat.id,text='Назначте колличество воинов, которые отправятся с оборонительных рубежей в резерв или введите "!", чтобы переместить в резерв всех воинов')
    units_define_dict[message.chat.id]='passive'

@dp.message(F.text=='⚔️НАЗАД⚔️')
async def back(message):
    keyboard=builder_main_menu.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Вы вернулись в главное меню',reply_markup=keyboard)
    if message.chat.id in list(units_define_dict.keys()):
        units_define_dict.pop(message.chat.id)
    if message.chat.id in list(units_attack_dict.keys()):
        units_attack_dict.pop(message.chat.id)
    if message.chat.id in list(medics_attack_dict.keys()):
        medics_attack_dict.pop(message.chat.id)

@dp.message(F.text=='🪙УЛУЧШЕНИЯ🪙')
async def upgrades_button_func(message):
    await account_check(message)
    keyboard=builder_upgrades.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Улучшать нашу промышленность - очень мудрое решение! Так мы станем более подготовленными и крепкими!',reply_markup=keyboard)

@dp.message(F.text=='🪙ЗОЛОТАЯ ШАХТА🪙')
async def gold_info(message):
    await account_check(message)
    cursor.execute('select gold_level from Users where chat_id=?',(message.chat.id,))
    info_gold_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении золотая шахта {info_gold_level} уровня, приносящая {gold_levels[info_gold_level]} монет в час')
    if info_gold_level!=10:
        keyboard=builder_gold.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить её вам потребуется {gold_prices[info_gold_level]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_gold2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень шахты максимальный!',reply_markup=keyboard)

@dp.message(F.text=='🪖ОБОРОНИТЕЛЬНЫЙ РУБЕЖ🪖')
async def defense_info(message):
    cursor.execute('select defense_level from Users where chat_id=?',(message.chat.id,))
    info_defense_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении оборонительный рубеж {info_defense_level} уровня, располагающий местами для {defense_levels[info_defense_level-1]} воинов')
    if info_defense_level!=10:
        keyboard=builder_defense.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить его вам потребуется {defense_prices[info_defense_level-1]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_defense2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень оборонительного рубежа максимальный!',reply_markup=keyboard)

@dp.message(F.text=='🪖БРОНЕТРАНСПОРТЁР🪖')
async def tank_info(message):
    cursor.execute('select tank_level from Users where chat_id=?',(message.chat.id,))
    info_tank_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении бронетранспортёр {info_tank_level} уровня, способный перевозить {tank_levels[info_tank_level-1]} воинов')
    if info_tank_level!=10:
        keyboard=builder_tank.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить его вам потребуется {tank_prices[info_tank_level-1]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_tank2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень бронетранспортёра максимальный!',reply_markup=keyboard)

@dp.message(F.text=='🏥МЕДИЦИНСКИЙ АВТОМОБИЛЬ🏥')
async def heal_auto_info(message):
    cursor.execute('select heal_auto_level from Users where chat_id=?',(message.chat.id,))
    info_heal_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении медицинский автомобиль {info_heal_level} уровня, способный перевозить {heal_auto_levels[info_heal_level]} медиков')
    if info_heal_level!=10:
        keyboard=builder_heal_auto.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить его вам потребуется {heal_auto_prices[info_heal_level]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_heal_auto2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень медицинского автомобиля максимальный!',reply_markup=keyboard)

@dp.message(F.text=='🪖ВОЕННАЯ ШКОЛА🪖')
async def heal_auto_info(message):
    cursor.execute('select war_school_level from Users where chat_id=?',(message.chat.id,))
    info_war_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении военная школа {info_war_level} уровня, выпускающая {war_school_levels[info_war_level]} воинов в час')
    if info_war_level!=10:
        keyboard=builder_war_school.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить её вам потребуется {war_school_prices[info_war_level]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_war_school2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень военной школы максимальный!',reply_markup=keyboard)

@dp.message(F.text=='🏥МЕДИЦИНСКАЯ ШКОЛА🏥')
async def heal_auto_info(message):
    cursor.execute('select medics_school_level from Users where chat_id=?',(message.chat.id,))
    info_heal_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении медицинская школа {info_heal_level} уровня, выпускающая {medics_school_levels[info_heal_level]} медиков в час')
    if info_heal_level!=10:
        keyboard=builder_medics_school.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить её вам потребуется {medics_school_prices[info_heal_level]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_medics_school2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень медицинской школы максимальный!',reply_markup=keyboard)

@dp.message(F.text=='🪙УЛУЧШИТЬ ЗОЛОТУЮ ШАХТУ🪙')
async def gold_upgrade(message):
    cursor.execute('select gold_level,gold from Users where chat_id=?',(message.chat.id,))
    info_gold=cursor.fetchall()[0]
    if info_gold[1]<gold_prices[info_gold[0]]:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
    else:
        keyboard=builder_gold2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен! Золотая шахта улучшена до {info_gold[0]+1} уровня!',reply_markup=keyboard)
        await bot.send_message(chat_id=message.chat.id,text=f'Теперь она приносит {gold_levels[info_gold[0]+1]} золотых монет в час!')
        builder_flag=False
        if info_gold[0]==9:
            builder_flag=True
            keyboard=builder_gold2.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text=f'Максимальный уровень!',reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Для следующего улучшения необходимо {gold_prices[info_gold[0]+1]}🪙')
        cursor.execute('update Users set xp=xp-?,gold_level=gold_level+1,gold=gold-? where chat_id=?',(gold_prices[info_gold[0]]//100,gold_prices[info_gold[0]],message.chat.id))
        connection.commit()
        await xp_count(message)
        if builder_flag:
            keyboard=builder_gold2.as_markup(resize_keyboard=True)
        else:
            keyboard=builder_gold.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Мы ждём вашего приказа, командир!',reply_markup=keyboard)

@dp.message(F.text=='🪙УЛУЧШИТЬ ОБОРОНИТЕЛЬНЫЙ РУБЕЖ🪙')
async def defense_upgrade(message):
    cursor.execute('select defense_level,gold from Users where chat_id=?',(message.chat.id,))
    info_defense=cursor.fetchall()[0]
    if info_defense[1]<defense_prices[info_defense[0]-1]:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
    else:
        keyboard=builder_defense2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен! Оборонительный рубеж улучшен до {info_defense[0]+1} уровня!',reply_markup=keyboard)
        await bot.send_message(chat_id=message.chat.id,text=f'Теперь на нём можно разместить максимум {defense_levels[info_defense[0]]} воинов!')
        builder_flag=False
        if info_defense[0]==9:
            builder_flag=True
            keyboard=builder_defense2.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text='Максимальный уровень!',reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Для следующего улучшения необходимо {defense_prices[info_defense[0]]}🪙')
        cursor.execute('update Users set xp=xp-?,defense_level=defense_level+1,units_defense_restriction=?,gold=gold-? where chat_id=?',(defense_prices[info_defense[0]-1]//100,defense_levels[info_defense[0]],defense_prices[info_defense[0]-1],message.chat.id))
        connection.commit()
        await xp_count(message)
        if builder_flag:
            keyboard=builder_defense2.as_markup(resize_keyboard=True)
        else:
            keyboard=builder_defense.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Мы ждём вашего приказа, командир!',reply_markup=keyboard)

@dp.message(F.text=='🪙УЛУЧШИТЬ БРОНЕТРАНСПОРТЁР🪙')
async def tank_upgrade(message):
    cursor.execute('select tank_level,gold from Users where chat_id=?',(message.chat.id,))
    info_tank=cursor.fetchall()[0]
    if info_tank[1]<tank_prices[info_tank[0]-1]:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
    else:
        keyboard=builder_tank2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен! Бронетранспортёр улучшен до {info_tank[0]+1} уровня!',reply_markup=keyboard)
        await bot.send_message(chat_id=message.chat.id,text=f'Теперь он может перевозить {tank_levels[info_tank[0]]} воинов!')
        builder_flag=False
        if info_tank[0]==9:
            builder_flag=True
            keyboard=builder_tank2.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text=f'Максимальный уровень!',reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Для следующего улучшения необходимо {tank_prices[info_tank[0]]}🪙')
        cursor.execute('update Users set xp=xp-?,tank_level=tank_level+1,units_attack_restriction=?,gold=gold-? where chat_id=?',(tank_prices[info_tank[0]-1]//100,tank_levels[info_tank[0]],tank_prices[info_tank[0]-1],message.chat.id))
        connection.commit()
        await xp_count(message)
        if builder_flag:
            keyboard=builder_tank2.as_markup(resize_keyboard=True)
        else:
            keyboard=builder_tank.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Мы ждём вашего приказа, командир!',reply_markup=keyboard)

@dp.message(F.text=='🪙УЛУЧШИТЬ МЕДИЦИНСКИЙ АВТОМОБИЛЬ🪙')
async def heal_auto_upgrade(message):
    cursor.execute('select heal_auto_level,gold from Users where chat_id=?',(message.chat.id,))
    info_heal=cursor.fetchall()[0]
    if info_heal[1]<heal_auto_prices[info_heal[0]]:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
    else:
        keyboard=builder_heal_auto2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен! Медицинский автомобиль улучшен до {info_heal[0]+1} уровня!',reply_markup=keyboard)
        await bot.send_message(chat_id=message.chat.id,text=f'Теперь он может перевозить {heal_auto_levels[info_heal[0]+1]} медиков!')
        builder_flag=False
        if info_heal[0]==9:
            builder_flag=True
            keyboard=builder_heal_auto2.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text=f'Максимальный уровень!',reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Для следующего улучшения необходимо {heal_auto_prices[info_heal[0]+1]}🪙')
        cursor.execute('update Users set xp=xp-?,heal_auto_level=heal_auto_level+1,medics_attack_restriction=?,gold=gold-? where chat_id=?',(heal_auto_prices[info_heal[0]-1]//100,heal_auto_levels[info_heal[0]+1],heal_auto_prices[info_heal[0]-1],message.chat.id))
        connection.commit()
        await xp_count(message)
        if builder_flag:
            keyboard=builder_heal_auto2.as_markup(resize_keyboard=True)
        else:
            keyboard=builder_heal_auto.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Мы ждём вашего приказа, командир!',reply_markup=keyboard)

@dp.message(F.text=='🪙УЛУЧШИТЬ ВОЕННУЮ ШКОЛУ🪙')
async def war_school_upgrade(message):
    cursor.execute('select war_school_level,gold from Users where chat_id=?',(message.chat.id,))
    info_war=cursor.fetchall()[0]
    if info_war[1]<war_school_prices[info_war[0]]:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
    else:
        keyboard=builder_war_school2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен! Военная школа улучшена до {info_war[0]+1} уровня!',reply_markup=keyboard)
        await bot.send_message(chat_id=message.chat.id,text=f'Теперь она выпускает {war_school_levels[info_war[0]+1]} воинов в час!')
        builder_flag=False
        if info_war[0]==9:
            builder_flag=True
            keyboard=builder_war_school2.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text=f'Максимальный уровень!',reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Для следующего улучшения необходимо {war_school_prices[info_war[0]+1]}🪙')
        cursor.execute('update Users set xp=xp-?,war_school_level=war_school_level+1,gold=gold-? where chat_id=?',(war_school_prices[info_war[0]]//100,war_school_prices[info_war[0]],message.chat.id))
        connection.commit()
        await xp_count(message)
        if builder_flag:
            keyboard=builder_war_school2.as_markup(resize_keyboard=True)
        else:
            keyboard=builder_war_school.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Мы ждём вашего приказа, командир!',reply_markup=keyboard)

@dp.message(F.text=='🪙УЛУЧШИТЬ МЕДИЦИНСКУЮ ШКОЛУ🪙')
async def war_school_upgrade(message):
    cursor.execute('select medics_school_level,gold from Users where chat_id=?',(message.chat.id,))
    info_heal=cursor.fetchall()[0]
    if info_heal[1]<medics_school_prices[info_heal[0]]:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
    else:
        keyboard=builder_medics_school2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен! Медицинская школа улучшена до {info_heal[0]+1} уровня!',reply_markup=keyboard)
        await bot.send_message(chat_id=message.chat.id,text=f'Теперь она выпускает {medics_school_levels[info_heal[0]+1]} медиков в час!')
        builder_flag=False
        if info_heal[0]==4:
            builder_flag=True
            keyboard=builder_medics_school2.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text=f'Максимальный уровень!',reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id,text=f'Для следующего улучшения необходимо {medics_school_prices[info_heal[0]+1]}🪙')
        cursor.execute('update Users set xp=xp-?,medics_school_level=medics_school_level+1,gold=gold-? where chat_id=?',(medics_school_prices[info_heal[0]]//100,medics_school_prices[info_heal[0]],message.chat.id))
        connection.commit()
        await xp_count(message)
        if builder_flag:
            keyboard=builder_medics_school2.as_markup(resize_keyboard=True)
        else:
            keyboard=builder_medics_school.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Мы ждём вашего приказа, командир!',reply_markup=keyboard)

@dp.message(F.text=='🪙СОБРАТЬ🪙')
async def gold_collect(message):
    if message.chat.id not in list(gold_count_dict.keys()):
        gold_count_dict[message.chat.id]=0
    cursor.execute('select gold_level from Users where chat_id=?',(message.chat.id,))
    info_gold_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Ваша шахта принесла нам {gold_count_dict[message.chat.id]*gold_levels[info_gold_level]} золотых монет!')
    cursor.execute('update Users set gold=gold+?*?',(gold_count_dict[message.chat.id],gold_levels[info_gold_level]))
    connection.commit()
    gold_count_dict[message.chat.id]=0

@dp.message(F.text=='⚔️ПЕРЕНАПРАВИТЬ ВОИНОВ В АРМИЮ⚔️')
async def war_school_units_collect(message):
    if message.chat.id not in list(war_school_count_dict.keys()):
        war_school_count_dict[message.chat.id]=0
    cursor.execute('select war_school_level from Users where chat_id=?',(message.chat.id,))
    info_war_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Из военной школы выпустились {war_school_count_dict[message.chat.id]*war_school_levels[info_war_level]} воинов!')
    cursor.execute('update Users set units_passive_number=units_passive_number+?*?',(war_school_count_dict[message.chat.id],war_school_levels[info_war_level]))
    connection.commit()
    war_school_count_dict[message.chat.id]=0

@dp.message(F.text=='⚔️ПЕРЕНАПРАВИТЬ МЕДИКОВ В АРМИЮ⚔️')
async def medics_school_units_collect(message):
    if message.chat.id not in list(medics_school_count_dict.keys()):
        medics_school_count_dict[message.chat.id]=0
    cursor.execute('select medics_school_level from Users where chat_id=?',(message.chat.id,))
    info_heal_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Из медицинской школы выпустились {medics_school_count_dict[message.chat.id]*medics_school_levels[info_heal_level]} медиков!')
    cursor.execute('update Users set medics_passive_number=medics_passive_number+?*?',(medics_school_count_dict[message.chat.id],medics_school_levels[info_heal_level]))
    connection.commit()
    medics_school_count_dict[message.chat.id]=0

@dp.message(F.text=='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️')
async def back_to_upgrades(message):
    keyboard=builder_upgrades.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Вы вернулись в меню улучшений',reply_markup=keyboard)

@dp.message(F.text=='⚔️НАПАСТЬ!⚔️')
async def attack(message):
    keyboard=builder_back.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Выберите колличество воинов из резерва, чтобы пойти в атаку или введите "!", чтобы заполнить бронетранспортёр до максимума.\nЕсли их не будет хватать, недостающая часть прибудет с оборонительных рубежей.',reply_markup=keyboard)
    units_attack_dict[message.chat.id]=0

@dp.message(F.text=='⭐🪙МАГАЗИН🪙⭐')
async def shop(message):
    keyboard=builder_shop.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Добро пожаловать в магазин!',reply_markup=keyboard)

@dp.message(F.text=='50🪖 за 100🪙')
async def buy_units(message):
    cursor.execute('select gold from Users where chat_id=?',(message.chat.id,))
    info_gold=cursor.fetchall()[0][0]
    if info_gold<100:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
        return
    cursor.execute('update Users set units_passive_number=units_passive_number+50,gold=gold-100 where chat_id=?',(message.chat.id,))
    connection.commit()
    await bot.send_message(chat_id=message.chat.id,text='Поздравляем с покупкой! Ваши воины доставлены в резерв!')

@dp.message(F.text=='20🏥 за 80🪙')
async def buy_medics(message):
    cursor.execute('select gold from Users where chat_id=?',(message.chat.id,))
    info_gold=cursor.fetchall()[0][0]
    if info_gold<80:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет!')
        return
    cursor.execute('update Users set medics_passive_number=medics_passive_number+20,gold=gold-80 where chat_id=?',(message.chat.id,))
    connection.commit()
    await bot.send_message(chat_id=message.chat.id,text='Поздравляем с покупкой! Ваши медики доставлены в резерв!')

@dp.message(F.text=='100🪖 за 49 ⭐')
async def buy_units_stars(message):
    order_id=message.from_user.username[:10]+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.answer_invoice(
        title='100 воинов',
        description='Совершая данную покупку, вы получаете 100 воинов в свой резерв!',
        currency='XTR',
        payload=order_id,
        prices=[LabeledPrice(label='100🪖',amount=49)])
    users_buy_dict[message.chat.id]=['units_passive_number',100,'100🪖',order_id]

@dp.message(F.text=='30🏥 за 59 ⭐')
async def buy_medics_stars(message):
    order_id=message.from_user.username[:10]+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.answer_invoice(
        title='30 медиков',
        description='Совершая данную покупку, вы получаете 30 медиков в свой резерв!',
        currency='XTR',
        payload=order_id,
        prices=[LabeledPrice(label='30🏥',amount=59)])
    users_buy_dict[message.chat.id]=['medic_passive_number',30,'30🏥',order_id]

@dp.message(F.text=='200🪙 за 39 ⭐')
async def buy_gold_stars(message):
    order_id=message.from_user.username[:10]+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.answer_invoice(
        title='200 золотых монет',
        description='Совершая данную покупку, вы получаете 200 золотых монет!',
        currency='XTR',
        payload=order_id,
        prices=[LabeledPrice(label='200🪙',amount=1)])
    users_buy_dict[message.chat.id]=['gold',200,'200🪙',order_id]

@dp.message(F.text=='1000🪙 за 119 ⭐')
async def buy_gold_much_stars(message):
    order_id=message.from_user.username[:10]+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await message.answer_invoice(
        title='1000 золотых монет',
        description='Совершая данную покупку, вы получаете 1000 золотых монет!',
        currency='XTR',
        payload=order_id,
        prices=[LabeledPrice(label='1000🪙',amount=119)])
    users_buy_dict[message.chat.id]=['gold',1000,'1000🪙',order_id]

@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query):
    info=None
    try:
        info=users_buy_dict[pre_checout_query.from_user.id][3]
    except:
        pass
    if info!=pre_checout_query.invoice_payload:
        await bot.send_message(chat_id=pre_checout_query.from_user.id,text='Данная платёжная заявка неактуальна!')
        if pre_checout_query.from_user.id in users_buy_dict.keys():
            users_buy_dict.pop(pre_checout_query.from_user.id)
        await pre_checkout_query.answer(ok=False)
        return
    await pre_checkout_query.answer(ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message):
    cursor.execute(f'update Users set {users_buy_dict[message.chat.id][0]}={users_buy_dict[message.chat.id][0]}+? where chat_id=?',
                   (users_buy_dict[message.chat.id][1],message.chat.id))
    connection.commit()
    await message.answer(f'Оплата произведена успешно! Вам зачислено {users_buy_dict[message.chat.id][2]}! Удачной игры!')
    users_buy_dict.pop(message.chat.id)

@dp.message(F.text=='🏆РЕЙТИНГ🏆')
async def rating(message):
    cursor.execute('select * from Users')
    info_users_number=cursor.fetchall()
    cursor.execute('select login,rating from Users order by rating desc limit ?',(len(info_users_number),))
    info_rating=cursor.fetchall()
    rating_text=''
    await bot.send_message(chat_id=message.chat.id,text='Рейтинг лучших игроков:')
    for i in range(len(info_rating)):
        if i==0:
            rating_text+=f'{i+1}.'+str(info_rating[i][0])+f'({str(info_rating[i][1])}🏆) - Император Ржавого Трона\n'
            continue
        rating_text+=f'{i+1}.'+str(info_rating[i][0])+f'({str(info_rating[i][1])}🏆)\n'
        if i==9:
            break
    await bot.send_message(chat_id=message.chat.id,text=rating_text)
    cursor.execute('select login,rating from Users where chat_id=?',(message.chat.id,))
    info_personal_rating=cursor.fetchall()
    await bot.send_message(chat_id=message.chat.id,text=f'Ваш рейтинг - {str(info_personal_rating[0][1])}🏆 ({info_rating.index(info_personal_rating[0])+1} место)')

@dp.message(F.text=='СТАТИСТИКА')
async def users_info_ADMIN(message):
    cursor.execute('select * from Users')
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в игре The Rusty Throne зарегистрировано {len(cursor.fetchall())} пользователей!')

@dp.message(F.text=='СООБЩЕНИЕ')
async def message_ADMIN(message):
    global admin_message_flag
    await bot.send_message(chat_id=message.chat.id,text='Введите текст сообщения')
    admin_message_flag='message'

@dp.message(F.text=='УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ')
async def delete_user_ADMIN(message):
    global admin_message_flag
    await bot.send_message(chat_id=message.chat.id,text='Введите логин пользователя')
    admin_message_flag='delete'

@dp.message(F.text=='ОТПРАВИТЬ ВОИНОВ')
async def send_units_ADMIN(message):
    global admin_message_flag
    await bot.send_message(chat_id=message.chat.id,text='Введите колличество воинов')
    admin_message_flag='units'

@dp.message(F.text=='ОТПРАВИТЬ МЕДИКОВ')
async def send_units_ADMIN(message):
    global admin_message_flag
    await bot.send_message(chat_id=message.chat.id,text='Введите колличество медиков')
    admin_message_flag='medics'

@dp.message(F.text=='ОТПРАВИТЬ ЗОЛОТО')
async def send_gold_ADMIN(message):
    global admin_message_flag
    await bot.send_message(chat_id=message.chat.id,text='Введите колличество золотых монет')
    admin_message_flag='gold'

@dp.message(F.text=='ВЫЙТИ')
async def exit_ADMIN(message):
    global admin_flag
    global admin_message_flag
    keyboard=builder_main_menu.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Вы вышли из меню администратора',reply_markup=keyboard)
    admin_flag=None
    admin_message_flag=None
    
@dp.message()
async def message_func(message):
    global admin_flag
    global admin_message_flag
    global units_attack_flags
    if message.from_user.username=='Igor_Tsvetkov_2007' and message.text.lower()=='admin':
        admin_flag=message.chat.id
        keyboard=builder_admin.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Вы вошли, как администратор!',reply_markup=keyboard)
        return
    if admin_flag==message.chat.id:
        if admin_message_flag=='message':
            cursor.execute('select chat_id from Users')
            info_chats=cursor.fetchall()
            messages_count=0
            for chat in info_chats:
                try:
                    await bot.send_message(chat_id=chat[0],text='СООБЩЕНИЕ ОТ АДМИНИСТРАТОРА:\n\n'+message.text+'\n\nПо всем вопросам обращаться ко мне лично: @Igor_Tsvetkov_2007')
                    messages_count+=1
                except:
                    continue
            await bot.send_message(chat_id=message.chat.id,text=f'Сообщение разослано {messages_count} пользователям!')
            admin_message_flag=None
        elif admin_message_flag=='delete':
            cursor.execute('select chat_id from Users where login=?',(message.text,))
            info_chat=cursor.fetchall()
            if len(info_chat)==0:
                await bot.send_message(chat_id=message.chat.id,text='Такого пользователя не существует!')
                return
            cursor.execute('delete from Users where login=?',(message.text,))
            connection.commit()
            await bot.send_message(chat_id=message.chat.id,text=f'Пользователь {message.text} Успешно удалён!')
            keyboard=builder_reload_bot.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=info_chat[0][0],text='Ваш профиль был удалён администратором!',reply_markup=keyboard)
            await bot.send_message(chat_id=info_chat[0][0],text='Перезапустите бота, чтобы начать игру заново!')
            if message.chat.id==info_chat[0][0]:
                admin_flag=None
                admin_message_flag=None
            if info_chat[0][0] in list(units_count_dict.keys()):
                units_count_dict.pop(info_chat[0][0])
            if info_chat[0][0] in list(units_define_dict.keys()):
                units_define_dict.pop(info_chat[0][0])
            if info_chat[0][0] in list(units_attack_dict.keys()):
                units_attack_dict.pop(info_chat[0][0])
            if info_chat[0][0] in list(gold_count_dict.keys()):
                gold_count_dict.pop(info_chat[0][0])
            admin_message_flag=None
        elif admin_message_flag=='units':
            cursor.execute('select chat_id from Users')
            info_chat=cursor.fetchall()
            units_number=0
            try:
                units_number=int(message.text)
            except:
                await bot.send_message(chat_id=message.chat.id,text='Неверный формат!')
                return
            units_count=0
            for chat in info_chat:
                try:
                    await bot.send_message(chat_id=chat[0],text=f'Подарок от администратора @Igor_Tsvetkov_2007:\n{units_number}🪖')
                    units_count+=1
                except:
                    continue
            await bot.send_message(chat_id=message.chat.id,text=f'Воины отправлены {units_count} пользователям!')
            cursor.execute('update Users set units_passive_number=units_passive_number+?',(units_number,))
            connection.commit()
            admin_message_flag=None
        elif admin_message_flag=='medics':
            cursor.execute('select chat_id from Users')
            info_chat=cursor.fetchall()
            medics_number=0
            try:
                medics_number=int(message.text)
            except:
                await bot.send_message(chat_id=message.chat.id,text='Неверный формат!')
                return
            units_count=0
            for chat in info_chat:
                try:
                    await bot.send_message(chat_id=chat[0],text=f'Подарок от администратора @Igor_Tsvetkov_2007:\n{medics_number}🏥')
                    units_count+=1
                except:
                    continue
            await bot.send_message(chat_id=message.chat.id,text=f'Медики отправлены {units_count} пользователям!')
            cursor.execute('update Users set medics_passive_number=medics_passive_number+?',(medics_number,))
            connection.commit()
            admin_message_flag=None
        elif admin_message_flag=='gold':
            cursor.execute('select chat_id from Users')
            info_chat=cursor.fetchall()
            gold_number=0
            try:
                gold_number=int(message.text)
            except:
                await bot.send_message(chat_id=message.chat.id,text='Неверный формат!')
                return
            gold_count=0
            for chat in info_chat:
                try:
                    await bot.send_message(chat_id=chat[0],text=f'Подарок от администратора @Igor_Tsvetkov_2007:\n{gold_number}🪙')
                    gold_count+=1
                except:
                    continue
            await bot.send_message(chat_id=message.chat.id,text=f'Золото отправлено {gold_count} пользователям!')
            cursor.execute('update Users set gold=gold+?',(gold_number,))
            connection.commit()
            admin_message_flag=None
        return
    if message.chat.id in list(units_define_dict.keys()):
        units_number=0
        if message.text!='!':
            try:
                units_number=int(message.text)
            except:
                await bot.send_message(chat_id=message.chat.id,text='Неверный формат! Введите число!')
                return
            if int(message.text)<1:
                await bot.send_message(chat_id=message.chat.id,text='Введите положительное число!')
                return
        if units_define_dict[message.chat.id]=='active':
            if message.text=='!':
                cursor.execute('select units_passive_number,units_active_number,units_defense_restriction from Users where chat_id=?',(message.chat.id,))
                info=cursor.fetchall()
                if info[0][0]>=info[0][2]-info[0][1]:
                    cursor.execute('update Users set units_active_number=units_defense_restriction,units_passive_number=units_passive_number-? where chat_id=?',(info[0][2]-info[0][1],message.chat.id))
                else:
                    cursor.execute('update Users set units_active_number=units_passive_number+units_active_number,units_passive_number=0 where chat_id=?',(message.chat.id,))
                    connection.commit()
                cursor.execute('select units_passive_number,units_active_number from Users where chat_id=?',(message.chat.id,))
                info_units=cursor.fetchall()
                await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен, командир!\nСейчес на рубежах находится {info_units[0][1]} воинов, а в резерве {info_units[0][0]} воинов')
                return
            cursor.execute('select units_passive_number,units_active_number,units_defense_restriction from Users where chat_id=?',(message.chat.id,))
            info_units=cursor.fetchall()
            if info_units[0][1]>info_units[0][2]:
                cursor.execute('update Users set units_active_number=units_defense_restriction where chat_id=?',(message.chat.id,))
                connection.commit()
            if units_number>info_units[0][0]:
                await bot.send_message(chat_id=message.chat.id,text='У вас нет такого колличества воинов в резерве!\nБыть реалистом - серьёзное преимущество в наше время!')
            else:
                if units_number<=info_units[0][2]-info_units[0][1]:
                    cursor.execute('update Users set units_passive_number=units_passive_number-?,units_active_number=units_active_number+? where chat_id=?',(units_number,units_number,message.chat.id))
                    cursor.execute('select units_passive_number,units_active_number from Users where chat_id=?',(message.chat.id,))
                    connection.commit()
                    info_units=cursor.fetchall()
                    await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен, командир!\nСейчес на оборонительном рубеже находится {info_units[0][1]} воинов, а в резерве {info_units[0][0]} воинов')
                else:
                    await bot.send_message(chat_id=message.chat.id,text='Столько воинов не поместятся на оборонительном рубеже, выберите другое колличество!')
            return
        elif units_define_dict[message.chat.id]=='passive':
            cursor.execute('select units_passive_number,units_active_number from Users where chat_id=?',(message.chat.id,))
            info=cursor.fetchall()
            if message.text=='!':
                cursor.execute('update Users set units_passive_number=units_passive_number+units_active_number,units_active_number=0 where chat_id=?',(message.chat.id,))
                cursor.execute('select units_passive_number,units_active_number from Users where chat_id=?',(message.chat.id,))
                connection.commit()
                info_units=cursor.fetchall()
                await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен, командир!\nСейчес на оборонительном рубеже находится {info_units[0][1]} воинов, а в резерве {info_units[0][0]} воинов')
                return
            if units_number<=info[0][1]:
                cursor.execute('update Users set units_passive_number=units_passive_number+?,units_active_number=units_active_number-? where chat_id=?',(units_number,units_number,message.chat.id))
                cursor.execute('select units_passive_number,units_active_number from Users where chat_id=?',(message.chat.id,))
                connection.commit()
                info_units=cursor.fetchall()
                await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен, командир!\nСейчес на оборонительном рубеже находится {info_units[0][1]} воинов, а в резерве {info_units[0][0]} воинов')
            else:
                await bot.send_message(chat_id=message.chat.id,text='У нас нет такого колличества воинов на оборонительном рубеже!\nБыть реалистом - серьёзное преимущество в наше время!\nОтдайте корректный приказ!')
            return
    elif message.chat.id in list(units_attack_dict.keys()):
        start_attack_flag=False
        units_number=0
        medics_number=0
        if message.chat.id not in list(medics_attack_dict.keys()):
            if message.text!='!':
                try:
                    units_number=int(message.text)
                except:
                    await bot.send_message(chat_id=message.chat.id,text='Неверный формат! Введите число!')
                    return
                if int(message.text)<1:
                    await bot.send_message(chat_id=message.chat.id,text='Введите положительное число!')
                    return
            cursor.execute('select units_passive_number,units_active_number,units_attack_restriction from Users where chat_id=?',(message.chat.id,))
            info=cursor.fetchall()
            if message.text=='!':
                if info[0][0]<info[0][2]:
                    if info[0][0]+info[0][1]>=info[0][2]:
                        units_attack_dict[message.chat.id]=info[0][2]
                        cursor.execute('update Users set units_passive_number=0,units_active_number=units_active_number-? where chat_id=?',(info[0][2]-info[0][0],message.chat.id))
                        connection.commit()
                    else:
                        units_attack_dict[message.chat.id]=info[0][0]+info[0][1]
                        cursor.execute('update Users set units_passive_number=0,units_active_number=0 where chat_id=?',(message.chat.id,))
                        connection.commit()
                else:
                    units_attack_dict[message.chat.id]=info[0][2]
                    cursor.execute('update Users set units_passive_number=units_passive_number-units_attack_restriction where chat_id=?',(message.chat.id,))
                    connection.commit()
            else:
                if units_number>info[0][2]:
                    await bot.send_message(chat_id=message.chat.id,text='Наш бронетранспортёр не настолько вместителен! Выберите другое колличество воинов!')
                    return
                if units_number>info[0][0]+info[0][1]:
                    await bot.send_message(chat_id=message.chat.id,text='У нас нет такого колличества воинов!\nКомандир амбициозен, но его приказ невыполним!')
                    return
                else:
                    units_attack_dict[message.chat.id]=units_number
                    if units_number<=info[0][0]:
                        cursor.execute('update Users set units_passive_number=? where chat_id=?',(info[0][0]-units_number,message.chat.id))
                    else:
                        cursor.execute('update Users set units_passive_number=0,units_active_number=? where chat_id=?',(units_number-info[0][0],message.chat.id))
                    connection.commit()
            cursor.execute('select heal_auto_level from Users where chat_id=?',(message.chat.id,))
            info_heal_level=cursor.fetchall()[0][0]
            if info_heal_level==0:
                medics_attack_dict[message.chat.id]=0
                start_attack_flag=True
            else:
                await bot.send_message(chat_id=message.chat.id,text='Выберите колличество медиков из резерва, чтобы повысить шансы воинов на выживание или введите "!", чтобы заполнить медицинский автомобиль до максимума')
                medics_attack_dict[message.chat.id]=None
        else:
            if message.text!='!':
                try:
                    medics_number=int(message.text)
                except:
                    await bot.send_message(chat_id=message.chat.id,text='Неверный формат! Введите число!')
                    return
                if int(message.text)<0:
                    await bot.send_message(chat_id=message.chat.id,text='Недопускается отрицательное число!')
                    return
            cursor.execute('select medics_passive_number,medics_attack_restriction from Users where chat_id=?',(message.chat.id,))
            info=cursor.fetchall()
            if message.text=='!':
                start_attack_flag=True
                if info[0][0]<info[0][1]:
                    medics_attack_dict[message.chat.id]=info[0][0]
                    cursor.execute('update Users set medics_passive_number=0 where chat_id=?',(message.chat.id,))
                    connection.commit()
                else:
                    medics_attack_dict[message.chat.id]=info[0][1]
                    cursor.execute('update Users set medics_passive_number=medics_passive_number-medics_attack_restriction where chat_id=?',(message.chat.id,))
                    connection.commit()
            else:
                if medics_number>info[0][1]:
                    await bot.send_message(chat_id=message.chat.id,text='Наш медицинский автомобиль не настолько вместителен! Выберите другое колличество медиков!')
                    return
                if medics_number>info[0][0]:
                    await bot.send_message(chat_id=message.chat.id,text='У нас нет такого колличества медиков!\nКомандир амбициозен, но его приказ невыполним!')
                    return
                else:
                    start_attack_flag=True
                    medics_attack_dict[message.chat.id]=medics_number
                    cursor.execute('update Users set medics_passive_number=? where chat_id=?',(info[0][0]-medics_number,message.chat.id))
                    connection.commit()
        if start_attack_flag==True:#НАЧИНАЕМ АТАКУ!!!!
            await bot.send_message(chat_id=message.chat.id,text=f'Приказ выполнен, командир!\nВ атаку готовы идти {units_attack_dict[message.chat.id]} воинов и {medics_attack_dict[message.chat.id]} медиков!')
            await bot.send_message(chat_id=message.chat.id,text='Ищем противника!')
            cursor.execute('select login,units_active_number,chat_id from Users where chat_id<>?',(message.chat.id,))
            enemies_list=cursor.fetchall()
            units_attack_flags.append(message.chat.id)
            j=0
            while j<len(enemies_list):
                try:
                    info_enemy=random.choice(enemies_list)
                    cursor.execute('select login from Users where chat_id=?',(message.chat.id,))
                    info_send=cursor.fetchall()
                    await bot.send_message(chat_id=info_enemy[2],text='Командир, на нас совершили нападение!')
                    await bot.send_message(chat_id=info_enemy[2],text=str(info_send[0][0]))
                    break
                except:
                    enemies_list.remove(info_enemy)
                    continue
            count=units_attack_dict[message.chat.id]/(info_enemy[1]+units_attack_dict[message.chat.id])
            count_fortune=random.uniform(0,1)
            await bot.send_message(chat_id=message.chat.id,text='Противник найден!')
            await bot.send_message(chat_id=message.chat.id,text=str(info_enemy[0]))
            await bot.send_message(chat_id=message.chat.id,text=f'На оборонительном рубеже противника находятся {info_enemy[1]} воинов!')
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка атаки.png'),caption='Идём в атаку!!!!')
            for i in range(random.randint(4,8)):
                await bot.send_message(chat_id=message.chat.id,text='⚔️')
                time.sleep(1)
            units_get=0
            gold_get=0
            keyboard=builder_main_menu.as_markup(resize_keyboard=True)
            if count_fortune<=count:
                units_get=random.randint(0,info_enemy[1])
                gold_get=random.randint(0,info_enemy[1])
                if units_get==1:
                    units_get=3
                if gold_get==0:
                    gold_get=random.randint(0,10)
                rating_get=random.randint(0,10)
                rating_loss_enemy=random.randint(0,5)
                await bot.send_message(chat_id=message.chat.id,text='АТАКА ПРОШЛА УСПЕШНО!!!!\nПОЗДРАВЛЯЕМ ВАС, КОМАНДИР!!!!',reply_markup=keyboard)
                await bot.send_message(chat_id=message.chat.id,text=f'Нам удалось взять в плен {units_get//3} воинов. Они будут сражаться за нас!')
                await bot.send_message(chat_id=message.chat.id,text=f'Нам удалось добыть {gold_get} золотых монет!')
                await bot.send_message(chat_id=message.chat.id,text=f'+{abs(units_get*50)+50}XP')
                await bot.send_message(chat_id=message.chat.id,text=f'+{rating_get}🏆')
                await bot.send_photo(chat_id=info_enemy[2],photo=FSInputFile('images/картинка прорыва обороны.png'),caption='Нашу оборону прорвали!')
                await bot.send_message(chat_id=info_enemy[2],text=f'Мы потеряли {units_get//2} воинов!')
                await bot.send_message(chat_id=info_enemy[2],text=f'Мы потеряли {gold_get} золотых монет!')
                await bot.send_message(chat_id=info_enemy[2],text=f'-{rating_loss_enemy}🏆')
                cursor.execute('update Users set units_passive_number=units_passive_number+?,gold=gold+? where chat_id=?',(units_get//3+units_attack_dict[message.chat.id],gold_get,message.chat.id))
                cursor.execute('update Users set units_active_number=units_active_number-?,rating=rating-?,gold=gold-? where chat_id=?',(units_get//2,rating_loss_enemy,gold_get//2,info_enemy[2]))
                cursor.execute('update Users set xp=xp-?,rating=rating+?,medics_passive_number=medics_passive_number+? where chat_id=?',
                               (abs(units_get*50)+50,rating_get,medics_attack_dict[message.chat.id],message.chat.id))
                cursor.execute('select rating,units_active_number from Users where chat_id=?',(info_enemy[2],))
                info_rating=cursor.fetchall()
                if info_rating[0][0]<0:
                    cursor.execute('update Users set rating=0 where chat_id=?',(info_enemy[2],))
                if info_rating[0][1]<0:
                    cursor.execute('update Users set units_active_number=0 where chat_id=?',(info_enemy[2],))
            else:
                units_get=-random.randint(0,units_attack_dict[message.chat.id])
                medics_get=-random.randint(0,medics_attack_dict[message.chat.id])//3
                heal_range=int(abs(units_get)/5*medics_attack_dict[message.chat.id])
                units_heal=random.randint(0,heal_range)
                while units_heal>=abs(units_get):
                    heal_range-=1
                    units_heal=random.randint(0,heal_range)
                if units_heal==0 and medics_attack_dict[message.chat.id]!=0:
                    units_heal=1
                units_get+=units_heal
                if units_get>0:
                    units_heal-=units_get
                    units_get=0
                await bot.send_message(chat_id=message.chat.id,text='АТАКА ЗАВЕРШИЛАСЬ НЕУДАЧНО!!!!',reply_markup=keyboard)
                await bot.send_message(chat_id=message.chat.id,text=f'Наши медики спасли {units_heal} воинов!')
                await bot.send_message(chat_id=message.chat.id,text=f'Мы потеряли {abs(units_get)} воинов!')
                await bot.send_message(chat_id=message.chat.id,text=f'Мы потеряли {abs(medics_get)} медиков!')
                await bot.send_message(chat_id=message.chat.id,text=f'+{abs(units_get)+50}XP')
                await bot.send_photo(chat_id=info_enemy[2],photo=FSInputFile('images/картинка успешной обороны.png'),caption='Наша оборона выдержала!')
                await bot.send_message(chat_id=info_enemy[2],text=f'Нам удалось взять в плен {abs(units_get//2)} воинов. Они будут сражаться за нас!')
                await bot.send_message(chat_id=info_enemy[2],text=f'Нам удалось взять в плен {abs(medics_get//2)} медиков. Они будут лечить наших людей!')
                cursor.execute('update Users set units_passive_number=units_passive_number+?,gold=gold+? where chat_id=?',(units_get+units_attack_dict[message.chat.id],gold_get,message.chat.id))  
                cursor.execute('update Users set units_passive_number=units_passive_number-? where chat_id=?',(units_get//2,info_enemy[2]))
                cursor.execute('update Users set xp=xp-? where chat_id=?',(abs(units_get)+50,message.chat.id))
                cursor.execute('update Users set medics_passive_number=medics_passive_number+? where chat_id=?',(medics_get+medics_attack_dict[message.chat.id],message.chat.id))
                cursor.execute('update Users set medics_passive_number=medics_passive_number-? where chat_id=?',(medics_get//2,info_enemy[2]))
                cursor.execute('select units_active_number from Users where chat_id=?',(message.chat.id,))
                info_rating=cursor.fetchall()
                if info_rating[0][0]<0:
                    cursor.execute('update Users set units_active_number=0 where chat_id=?',(message.chat.id,))
            await xp_count(message)
            cursor.execute('select units_passive_number,units_active_number,gold,medics_passive_number from Users where chat_id=?',(info_enemy[2],))
            info_check=cursor.fetchall()
            if info_check[0][0]<0:
                cursor.execute('update Users set units_passive_number=0 where chat_id=?',(info_enemy[0][2],))
            if info_check[0][1]<0:
                cursor.execute('update Users set units_active_number=0 where chat_id=?',(info_enemy[0][2],))
            if info_check[0][2]<0:
                cursor.execute('update Users set gold=0 where chat_id=?',(info_enemy[0][2],))
            if info_check[0][3]<0:
                cursor.execute('update Users set medics_passive_number=0 where chat_id=?',(info_enemy[0][2],))
            connection.commit()
            units_attack_flags.remove(message.chat.id)
            medics_attack_dict.pop(message.chat.id)
    cursor.execute('select login from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()
    if info[0][0]==None:
        if len(message.text)<1 or len(message.text)>20:
            await bot.send_message(chat_id=message.chat.id,text='Некорректное имя! Длина должна составлять от 1 до 20 символов')
        else:
            cursor.execute('select login from Users')
            info_logins=cursor.fetchall()
            if (message.text,) in info_logins:
                await bot.send_message(chat_id=message.chat.id,text='Командир с таким именем уже существует! Чтобы войти в историю, вам необходимо быть уникальным!')
                await bot.send_message(chat_id=message.chat.id,text='Пожалуйста, придумайте другое имя!')
                return
            keyboard=builder_main_menu.as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.chat.id,text=f'Добро пожаловать в крепость, {message.text}',reply_markup=keyboard)
            cursor.execute('update Users set login=? where chat_id=?',(message.text,message.chat.id))
            cursor.execute('select login,chat_id from Users')
            info_logins=cursor.fetchall()
            for i in range(len(info_logins)):
                if info_logins[i][0]==None:
                    try:
                        cursor.execute('delete from Users where chat_id=?',(info_logins[i][1]))
                        connection.commit()
                        await bot.send_message(chat_id=info_logins[i][1],text='Вы были автоматически удалены из базы данных из-за некорректного логина!')
                    except:
                        continue
            connection.commit()

asyncio.run(main())
