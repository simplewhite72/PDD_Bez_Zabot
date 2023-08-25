import sqlite3
from configs import config

def write_question_to_db(file_id:str, question_string:str, question_caption: str) :
    
    con = sqlite3.connect(config.database_file_path)
    cursor = con.cursor()
    
    questions = question_string.split()
    for question in questions :
        bilet_num=int(question[0:2])
        question_num=int(question[2:4])
        title = "Билет " + question[0:2] + ", вопрос "+ question[2:4]
        dict_str = (file_id, question_caption, title, bilet_num, question_num)
        cursor.execute("UPDATE question SET video_file_id=?, caption=?, title=? WHERE paper_id=? AND paper_order=?", dict_str)
        con.commit()
    
    cursor.close()


def delete_question_from_db(question_string:str) :
    
    con = sqlite3.connect(config.database_file_path)
    cursor = con.cursor()
    
    questions = question_string.split()
    for question in questions :
        bilet_num=int(question[0:2])
        question_num=int(question[2:4])
        dict_str = (bilet_num, question_num)
        cursor.execute("UPDATE question SET video_file_id=NULL, caption=NULL, title=NULL WHERE paper_id=? AND paper_order=?", dict_str)
        con.commit()
    
    cursor.close()