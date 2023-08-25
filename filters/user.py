
from aiogram.filters import BaseFilter
from aiogram.types import Message

       
class UserTypeFilter(BaseFilter):  # [1]
    def __init__(self, user_id: str): # [2]
        self.user_id = user_id

    async def __call__(self, message: Message) -> bool:  # [3]
        if str(message.from_user.id) == self.user_id :
            return False
        else:
            return True