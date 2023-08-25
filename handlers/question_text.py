from aiogram import Router, F
from aiogram.types import Message
from functions import save_stat
from configs import config
import logging
from keyboards.for_questions import donate_kb
import datetime
from typing import Dict
from filters.user import UserTypeFilter
from filters.question import QuestionTypeFilter

router = Router()
router.message.filter(
                    UserTypeFilter(user_id=config.admin_id)
                    )

@router.message(F.text, QuestionTypeFilter(str(F.Text),config.output_df))
async def message_with_text(message: Message, output: Dict[str, str]):
    
    #Logging
    username = str(message.from_user.username)
    first_name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    user_id = str(message.from_user.id)
    fullusername = user_id +', '+ username +', ' +first_name+' ' + last_name
    logging.info('User:'+fullusername+'. Message: '+message.text)

    s = output['video_file_id']
    cap = "<b>"+output['title']+"</b>" + "\n\n"+ output['caption'] + "\n\n" + u'\U00002705' +config.LINK_1 + "\n" +  u'\U00002705' + config.LINK_2
    dt = datetime.datetime.now()
    now_time = dt.strftime('%H:%M:%S')
    now_date = dt.strftime('%m.%d.%Y')
    response = (now_date,now_time,user_id,username,first_name,last_name,int(message.text[0:2]),int(message.text[2:4]))
    save_stat.write_to_stat(response)
    if s == 'None' :
        await message.answer('Запрошенный вопрос еще не появился...')   
    else :
        await message.answer_video(video=s, 
                                   width=1920, 
                                   height=1080, 
                                   caption=cap, 
                                   supports_streaming=True,
                                   parse_mode='HTML'
                                   )
        
@router.message(F.text)
async def test_questions(message: Message):
    await message.answer('Введите вопрос в формате ББВВ, пожалуйста')         



