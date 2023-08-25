import sqlite3
from configs import config


def write_to_stat(dict):

    cursor = config.stat.cursor()
 
    # данные для добавления
    response = dict
    cursor.execute("INSERT INTO responses (date, time, user_id, username, first_name, last_name, bilet, question) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", response)
 
    config.stat.commit()
    cursor.close()

#def get_from_stat() :
#    cursor = config.stat.cursor()

