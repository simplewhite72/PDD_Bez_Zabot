from aiogram import Router
from aiogram import types
from configs import config
from typing import Dict
import hashlib
from keyboards import for_questions
from functions.question_filter import check_question

router = Router()

@router.inline_query()
async def inline_with_text(query: types.InlineQuery):
    text = query.query
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    if len(text) == 4 :
        
        output = check_question(text, config.output_df)
        s = output['video_file_id']
        cap = output['caption'] + "\n\n" + u'\U00002705' +config.LINK_1 + "\n" +  u'\U00002705' + config.LINK_2
        tit = output['title']
        articles = [types.InlineQueryResultCachedVideo(
            id = result_id,
            title = tit,
            description = cap,
            video_file_id = s,
            reply_markup = for_questions.inline_kb())]

      
        await query.answer(articles, cache_time = 1, is_personal=True)
    


