import sqlite3
import pandas
import logging
from dotenv import load_dotenv
import os
import numpy as np
from aiogram import Bot

load_dotenv()

#Secure links
token = os.environ.get("TOKEN")
admin_username = os.environ.get("ADMIN_USERNAME")
admin_id = os.environ.get("ADMIN_ID")


bot = Bot(token)
database_file_path = './database/paper.db'
statistics_file_path = './database/statistics.db'
donate_link = "https://yoomoney.ru/to/4100110106011403"
temp_file_path = 'temp.png'
NO_ADMIN_VIDEO = 'Я не знаю, что делать с видеофайлами :confused:'
bot_link = 'https://t.me/PDD_bez_zabot'
admin_link = 'https://vk.com/pistsovanatoly'
type_error = 'Ты скидываешь мне что-то не то...'
LINK_1 = f' Получи <u>видеоразбор</u> у ПДД бота: <a href="{bot_link}"><b>@PDD_Bez_Zabot</b></a>'
LINK_2 = f' Или напиши автору в ВК: <a href="{admin_link}"><b>Анатолий Писцов</b></a>'
LINK_ADMIN = '<b> ОТВЕТ ДЛЯ АДМИНА</b>'



con = sqlite3.connect(database_file_path)
cursorObj = con.cursor()
cursorObj.execute('SELECT paper_id, paper_order, text, answer1, answer2, answer3, answer4, video_file_id, caption, title, thumb FROM "question" WHERE category_id = 0')
database_names = list(map(lambda x: x[0], cursorObj.description))
rows = cursorObj.fetchall()
output_df = pandas.DataFrame (rows, columns = database_names)
output_df = output_df.replace ( r'^\s\*$' , np.nan , regex= True )
con.close()


stat = sqlite3.connect(statistics_file_path)

logging.basicConfig(level=logging.INFO, filename="./bot_log.log",
                    format="%(asctime)s %(levelname)s %(message)s")
