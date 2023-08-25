from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union, Dict
from functions.question_filter import check_question

class QuestionTypeFilter(BaseFilter):  # [1]
    def __init__(self, text: str, df): # [2]
        self.text = text
        self.df = df
                
    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        output = check_question(message.text, self.df)
        if output['video_file_id'] == "Type_Error" :
            return False
        else :
            return {"output": output}

