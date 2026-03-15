from aiogram import Bot,Dispatcher,F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message,KeyboardButton,FSInputFile,LabeledPrice,PreCheckoutQuery
import sqlite3
import asyncio
from threading import Thread
import time
import random

BOT_TOKEN='7734630132:AAGyqSg76roG5s0DUmeOEsf1S_Zld_5F350'
#YOOKASSA_TOKEN='381764678:TEST:130585'

bot=Bot(BOT_TOKEN)
dp=Dispatcher()

connection=sqlite3.connect('database.db')
cursor=connection.cursor()

cursor.execute('''create table if not exists Users(
                  chat_id Intager not null primary key,
                  login Varchar(20),
                  level Intager not null,
                  rating Intager not null,
                  xp Intager not null,
                  gold Intager not null,
                  gold_level Intager not null,
                  defense_level Intager not null,
                  war_school_level Intager not null,
                  tank_level Intager not null,
                  medics_school_level not null,
                  heal_auto_level Intager not null,
                  units_passive_number Intager not null,
                  units_active_number Intager not null,
                  units_defense_restriction Intager not null,
                  units_attack_restriction Intager not null,
                  medics_passive_number Intager not null,
                  medics_attack_restriction Intager not null)''')
connection.commit()

units_count_dict={}
war_school_count_dict={}
medics_school_count_dict={}
units_define_dict={}
units_attack_dict={}
medics_attack_dict={}
units_attack_flags=[]
gold_count_dict={}

xp_levels=(10,20,50,100,250,500,1000,1500,2000,3000,5000,7500,10000,12500,15000,17500,20000,25000,30000,40000,50000,60000,70000,80000,90000,100000,120000,150000,200000)

gold_levels=(0,1,2,4,6,8,12,15,20,30,50)
gold_prices=(5,10,50,100,500,600,800,1000,2000,3000,0)
defense_levels=(10,15,20,25,30,40,50,65,80,100)
defense_prices=(10,50,100,500,600,800,1000,2000,3000,0)
war_school_levels=(0,1,2,3,4,5,6,7,8,9,10)
war_school_prices=(20,30,50,100,300,500,800,1000,2000,3000,0)
tank_levels=(10,15,20,25,30,40,50,65,80,100)
tank_prices=(10,100,500,600,800,1000,3000,4000,5000,0)
medics_school_levels=(0,1,2,3,4,5)
medics_school_prices=(100,500,1000,2000,5000,0)
heal_auto_levels=(0,1,2,3,4,5,6,7,8,9,10)
heal_auto_prices=(100,200,300,500,600,800,1000,2000,4000,5000,0)

admin_flag=None
admin_message_flag=None

builder_start=ReplyKeyboardBuilder()
builder_start.row(KeyboardButton(text='⚔ДА! Я ГОТОВ!⚔'))

builder_begin_game=ReplyKeyboardBuilder()
builder_begin_game.row(KeyboardButton(text='⚔️ВПЕРЁД!⚔️'))

builder_main_menu=ReplyKeyboardBuilder()
builder_main_menu.row(KeyboardButton(text='⚔️ИНФОРМАЦИЯ⚔️'),KeyboardButton(text='⚔️НАПАСТЬ!⚔️'))
builder_main_menu.row(KeyboardButton(text='⚔️РАСПРЕДЕЛЕНИЕ ВОЙСК⚔️'),KeyboardButton(text='🪙УЛУЧШЕНИЯ🪙'))
builder_main_menu.row(KeyboardButton(text='⭐РЕЙТИНГ⭐'))
builder_main_menu.row(KeyboardButton(text='🪙МАГАЗИН🪙'))

builder_upgrades=ReplyKeyboardBuilder()
builder_upgrades.row(KeyboardButton(text='ОБОРОНИТЕЛЬНЫЙ РУБЕЖ'))
builder_upgrades.row(KeyboardButton(text='БРОНЕТРАНСПОРТЁР'))
builder_upgrades.row(KeyboardButton(text='МЕДИЦИНСКИЙ АВТОМОБИЛЬ'))
builder_upgrades.row(KeyboardButton(text='ВОЕННАЯ ШКОЛА'))
builder_upgrades.row(KeyboardButton(text='МЕДИЦИНСКАЯ ШКОЛА'))
builder_upgrades.row(KeyboardButton(text='ЗОЛОТАЯ ШАХТА'))
builder_upgrades.row(KeyboardButton(text='⚔️НАЗАД⚔️'))

builder_gold=ReplyKeyboardBuilder()
builder_gold.row(KeyboardButton(text='🪙УЛУЧШИТЬ ЗОЛОТУЮ ШАХТУ🪙'))
builder_gold.row(KeyboardButton(text='🪙СОБРАТЬ🪙'))
builder_gold.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_gold2=ReplyKeyboardBuilder()
builder_gold2.row(KeyboardButton(text='🪙СОБРАТЬ🪙'))
builder_gold2.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_war_school=ReplyKeyboardBuilder()
builder_war_school.row(KeyboardButton(text='🪙УЛУЧШИТЬ ВОЕННУЮ ШКОЛУ🪙'))
builder_war_school.row(KeyboardButton(text='⚔️ПЕРЕНАПРАВИТЬ ВОИНОВ В АРМИЮ⚔️'))
builder_war_school.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_war_school2=ReplyKeyboardBuilder()
builder_war_school2.row(KeyboardButton(text='⚔️ПЕРЕНАПРАВИТЬ ВОИНОВ В АРМИЮ⚔️'))
builder_war_school2.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_medics_school=ReplyKeyboardBuilder()
builder_medics_school.row(KeyboardButton(text='🪙УЛУЧШИТЬ МЕДИЦИНСКУЮ ШКОЛУ🪙'))
builder_medics_school.row(KeyboardButton(text='⚔️ПЕРЕНАПРАВИТЬ МЕДИКОВ В АРМИЮ⚔️'))
builder_medics_school.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_medics_school2=ReplyKeyboardBuilder()
builder_medics_school2.row(KeyboardButton(text='⚔️ПЕРЕНАПРАВИТЬ МЕДИКОВ В АРМИЮ⚔️'))
builder_medics_school2.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_defense=ReplyKeyboardBuilder()
builder_defense.row(KeyboardButton(text='🪙УЛУЧШИТЬ ОБОРОНИТЕЛЬНЫЙ РУБЕЖ🪙'))
builder_defense.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_defense2=ReplyKeyboardBuilder()
builder_defense2.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_tank=ReplyKeyboardBuilder()
builder_tank.row(KeyboardButton(text='🪙УЛУЧШИТЬ БРОНЕТРАНСПОРТЁР🪙'))
builder_tank.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_tank2=ReplyKeyboardBuilder()
builder_tank2.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_heal_auto=ReplyKeyboardBuilder()
builder_heal_auto.row(KeyboardButton(text='🪙УЛУЧШИТЬ МЕДИЦИНСКИЙ АВТОМОБИЛЬ🪙'))
builder_heal_auto.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_heal_auto2=ReplyKeyboardBuilder()
builder_heal_auto2.row(KeyboardButton(text='⚔️НАЗАД К УЛУЧШЕНИЯМ⚔️'))

builder_units_define=ReplyKeyboardBuilder()
builder_units_define.row(KeyboardButton(text='⚔️НАЗНАЧИТЬ ВОЙСКА ИЗ РЕЗЕРВА⚔️'))
builder_units_define.row(KeyboardButton(text='⚔️ОТОЗВАТЬ ВОЙСКА В РЕЗЕРВ⚔️'))
builder_units_define.row(KeyboardButton(text='⚔️НАЗАД⚔️'))

builder_shop=ReplyKeyboardBuilder()
builder_shop.row(KeyboardButton(text='50🪖 за 100🪙'),KeyboardButton(text='300🪖 за 499🪙'))
builder_shop.row(KeyboardButton(text='100🪖 за 30 руб.'),KeyboardButton(text='100🪙 за 79 руб.'))
builder_shop.row(KeyboardButton(text='⚔️НАЗАД⚔️'))

''',KeyboardButton(text='100🪙 за 79 руб.')'''

builder_reload_bot=ReplyKeyboardBuilder()
builder_reload_bot.row(KeyboardButton(text='ПЕРЕЗАПУСТИТЬ БОТА'))

builder_back=ReplyKeyboardBuilder()
builder_back.row(KeyboardButton(text='⚔️НАЗАД⚔️'))

builder_admin=ReplyKeyboardBuilder()
builder_admin.row(KeyboardButton(text='СТАТИСТИКА'))
builder_admin.row(KeyboardButton(text='СООБЩЕНИЕ'))
builder_admin.row(KeyboardButton(text='УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ'))
builder_admin.row(KeyboardButton(text='ОТПРАВИТЬ ВОИНОВ'))
builder_admin.row(KeyboardButton(text='ОТПРАВИТЬ МЕДИКОВ'))
builder_admin.row(KeyboardButton(text='ОТПРАВИТЬ ЗОЛОТО'))
builder_admin.row(KeyboardButton(text='ВЫЙТИ'))

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

async def main():
    Thread(target=units_count).start()
    await dp.start_polling(bot)

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
        cursor.execute('update Users set units_active_number=0 where chat_id=?',(message.chat.id))
        connection.commit()

@dp.message(F.text=='ПЕРЕЗАПУСТИТЬ БОТА')
async def bot_reload(message):
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
    keyboard=builder_units_define.as_markup(resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка распределения войск.png'),caption='Войска ждут вашего приказа, командир!',reply_markup=keyboard)
    #await bot.send_message(chat_id=message.chat.id,text='Войска ждут вашего приказа, командир!')
    
@dp.message(F.text=='⚔️НАЗНАЧИТЬ ВОЙСКА ИЗ РЕЗЕРВА⚔️')
async def units_active_direct(message):
    cursor.execute('select units_active_number,units_defense_restriction,units_passive_number from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас на оборонительных рубежах находится {info[0][0]} воинов (максимум {info[0][1]}), в резерве {info[0][2]} воинов')
    await bot.send_message(chat_id=message.chat.id,text='Назначте колличество воинов, которые отправятся из резерва в оборону или введите "!", чтобы заполнить рубежи до максимума.')
    units_define_dict[message.chat.id]='active'

@dp.message(F.text=='⚔️ОТОЗВАТЬ ВОЙСКА В РЕЗЕРВ⚔️')
async def units_passive_direct(message):
    cursor.execute('select units_active_number,units_passive_number from Users where chat_id=?',(message.chat.id,))
    info=cursor.fetchall()
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас на оборонительных рубежах находится {info[0][0]} воинов, в резерве {info[0][1]}')
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
    keyboard=builder_upgrades.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Улучшать нашу промышленность - очень мудрое решение! Так мы станем более подготовленными и крепкими!',reply_markup=keyboard)

@dp.message(F.text=='ЗОЛОТАЯ ШАХТА')
async def gold_info(message):
    cursor.execute('select gold_level from Users where chat_id=?',(message.chat.id,))
    info_gold_level=cursor.fetchall()[0][0]
    await bot.send_message(chat_id=message.chat.id,text=f'Сейчас в вашем распоряжении золотая шахта {info_gold_level} уровня, приносящая {gold_levels[info_gold_level]} монет в час')
    if info_gold_level!=10:
        keyboard=builder_gold.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text=f'Чтобы улучшить её вам потребуется {gold_prices[info_gold_level]} золотых монет',reply_markup=keyboard)
    else:
        keyboard=builder_gold2.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.chat.id,text='Уровень шахты максимальный!',reply_markup=keyboard)

@dp.message(F.text=='ОБОРОНИТЕЛЬНЫЙ РУБЕЖ')
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

@dp.message(F.text=='БРОНЕТРАНСПОРТЁР')
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

@dp.message(F.text=='МЕДИЦИНСКИЙ АВТОМОБИЛЬ')
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

@dp.message(F.text=='ВОЕННАЯ ШКОЛА')
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

@dp.message(F.text=='МЕДИЦИНСКАЯ ШКОЛА')
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

@dp.message(F.text=='🪙МАГАЗИН🪙')
async def shop(message):
    keyboard=builder_shop.as_markup(resize_keyboard=True)
    await bot.send_message(chat_id=message.chat.id,text='Добро пожаловать в магазин!',reply_markup=keyboard)

@dp.message(F.text=='50🪖 за 100🪙')
async def buy_units(message):
    cursor.execute('select gold from Users where chat_id=?',(message.chat.id,))
    info_gold=cursor.fetchall()
    if info_gold[0][0]<100:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет')
        return
    await bot.send_message(chat_id=message.chat.id,text='Покупка успешно совершена!')
    cursor.execute('update Users set units_passive_number=units_passive_number+50,gold=gold-100 where chat_id=?',(message.chat.id,))
    connection.commit()

@dp.message(F.text=='300🪖 за 499🪙')
async def buy_units2(message):
    cursor.execute('select gold from Users where chat_id=?',(message.chat.id,))
    info_gold=cursor.fetchall()
    if info_gold[0][0]<499:
        await bot.send_message(chat_id=message.chat.id,text='Недостаточно монет')
        return
    await bot.send_message(chat_id=message.chat.id,text='Покупка успешно совершена!')
    cursor.execute('update Users set units_passive_number=units_passive_number+300,gold=gold-499 where chat_id=?',(message.chat.id,))
    connection.commit()
'''
@dp.message(F.text=='100🪖 за 30 руб.')
async def buy_units_rub(message):
    title = '100 воинов'
    description = "Получите 100 воинов всего за 30 рублей!"
    payload = '100 units'
    currency = 'RUB'
    prices = [LabeledPrice(label='100 воинов', amount=10000)]
    await message.bot.send_invoice(chat_id=message.chat.id,title=title,description=description,payload=payload,provider_token=YOOKASSA_TOKEN,
                                   currency=currency,prices=prices,need_name=False,need_phone_number=False)


@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_payment(message):
    await message.answer("✅ Оплата прошла! Спасибо!")
'''
@dp.message(F.text=='⭐РЕЙТИНГ⭐')
async def buy_units2(message):
    cursor.execute('select * from Users')
    info_users_number=cursor.fetchall()
    cursor.execute('select login,rating from Users order by rating desc limit ?',(len(info_users_number),))
    info_rating=cursor.fetchall()
    rating_text=''
    await bot.send_message(chat_id=message.chat.id,text='Рейтинг лучших игроков:')
    for i in range(len(info_rating)):
        if i==0:
            rating_text+=f'{i+1}.'+str(info_rating[i][0])+f'({str(info_rating[i][1])}⭐) - Император Ржавого Трона\n'
            continue
        rating_text+=f'{i+1}.'+str(info_rating[i][0])+f'({str(info_rating[i][1])}⭐)\n'
        if i==9:
            break
    await bot.send_message(chat_id=message.chat.id,text=rating_text)
    cursor.execute('select login,rating from Users where chat_id=?',(message.chat.id,))
    info_personal_rating=cursor.fetchall()
    await bot.send_message(chat_id=message.chat.id,text=f'Ваш рейтинг - {str(info_personal_rating[0][1])}⭐ ({info_rating.index(info_personal_rating[0])+1} место)')

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
    if message.text=='Igor_2007_Admin_The_Rusty_Throne_2025':
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
                    await bot.send_message(chat_id=chat[0],text='СООБЩЕНИЕ ОТ АДМИНИСТРАТОРА:\n\n'+message.text+'\n\nПо всем вопросам обращаться ко мне лично: @Igor_Tsvetkov_2007\nЕсли Ты желаешь меня поддержать, то буду только рад! (89188933340 Сбер Игорь Валерьевич Ц.)')
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
                    #cursor.execute('update Users set units_active_number=units_passive_number,units_passive_number=0 where chat_id=?',(message.chat.id,))
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
    elif message.chat.id in list(units_attack_dict.keys()):# and (message.chat.id not in units_attack_flags or message.chat.id in list(medics_attack_dict.keys()))
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
            await bot.send_message(chat_id=info_enemy[2],text=info_send[0][0])
            count=units_attack_dict[message.chat.id]/(info_enemy[1]+units_attack_dict[message.chat.id])
            count_fortune=random.uniform(0,1)
            await bot.send_message(chat_id=message.chat.id,text='Противник найден!')
            await bot.send_message(chat_id=message.chat.id,text=str(info_enemy[0]))
            await bot.send_message(chat_id=message.chat.id,text=f'На оборонительном рубеже противника находится {info_enemy[1]} воинов!')
            #await bot.send_message(chat_id=message.chat.id,text='Идём в атаку!!!!')
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile('images/картинка атаки.png'),caption='Идём в атаку!!!!')
            for i in range(random.randint(4,8)):
                await bot.send_message(chat_id=message.chat.id,text='⚔️')
                time.sleep(1)
            units_get=0
            gold_get=0
            '''
            cursor.execute('select login from Users where chat_id=?',(message.chat.id,))
            info_send=cursor.fetchall()
            await bot.send_message(chat_id=info_enemy[2],text='Командир, на нас совершили нападение!')
            await bot.send_message(chat_id=info_enemy[2],text=info_send[0][0])
            '''
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
                await bot.send_message(chat_id=message.chat.id,text=f'+{rating_get}⭐')
                #await bot.send_message(chat_id=info_enemy[2],text='Нашу оборону прорвали!')
                await bot.send_photo(chat_id=info_enemy[2],photo=FSInputFile('images/картинка прорыва обороны.png'),caption='Нашу оборону прорвали!')
                await bot.send_message(chat_id=info_enemy[2],text=f'Мы потеряли {units_get//2} воинов!')
                await bot.send_message(chat_id=info_enemy[2],text=f'Мы потеряли {gold_get} золотых монет!')
                await bot.send_message(chat_id=info_enemy[2],text=f'-{rating_loss_enemy}⭐')
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
