from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
import sqlite3
import os

BOT_TOKEN='7734630132:AAGyqSg76roG5s0DUmeOEsf1S_Zld_5F350'

dir_path=os.path.dirname(os.path.abspath(__file__))

connection=sqlite3.connect(os.path.join(dir_path,'TRT_database.db'))
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

builder_start=ReplyKeyboardBuilder()
builder_start.row(KeyboardButton(text='⚔ДА! Я ГОТОВ!⚔'))

builder_begin_game=ReplyKeyboardBuilder()
builder_begin_game.row(KeyboardButton(text='⚔️ВПЕРЁД!⚔️'))

builder_main_menu=ReplyKeyboardBuilder()
builder_main_menu.row(KeyboardButton(text='⚔️ИНФОРМАЦИЯ⚔️'),KeyboardButton(text='⚔️НАПАСТЬ!⚔️'))
builder_main_menu.row(KeyboardButton(text='⚔️РАСПРЕДЕЛЕНИЕ ВОЙСК⚔️'),KeyboardButton(text='🪙УЛУЧШЕНИЯ🪙'))
builder_main_menu.row(KeyboardButton(text='🏆РЕЙТИНГ🏆'))
builder_main_menu.row(KeyboardButton(text='⭐🪙МАГАЗИН🪙⭐'))

builder_upgrades=ReplyKeyboardBuilder()
builder_upgrades.row(KeyboardButton(text='🪖ОБОРОНИТЕЛЬНЫЙ РУБЕЖ🪖'))
builder_upgrades.row(KeyboardButton(text='🪖БРОНЕТРАНСПОРТЁР🪖'))
builder_upgrades.row(KeyboardButton(text='🏥МЕДИЦИНСКИЙ АВТОМОБИЛЬ🏥'))
builder_upgrades.row(KeyboardButton(text='🪖ВОЕННАЯ ШКОЛА🪖'))
builder_upgrades.row(KeyboardButton(text='🏥МЕДИЦИНСКАЯ ШКОЛА🏥'))
builder_upgrades.row(KeyboardButton(text='🪙ЗОЛОТАЯ ШАХТА🪙'))
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
builder_shop.row(KeyboardButton(text='50🪖 за 100🪙'),KeyboardButton(text='20🏥 за 80🪙'))
builder_shop.row(KeyboardButton(text='100🪖 за 49 ⭐'),KeyboardButton(text='30🏥 за 59 ⭐'))
builder_shop.row(KeyboardButton(text='200🪙 за 39 ⭐'),KeyboardButton(text='1000🪙 за 119 ⭐'))
builder_shop.row(KeyboardButton(text='⚔️НАЗАД⚔️'))

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
