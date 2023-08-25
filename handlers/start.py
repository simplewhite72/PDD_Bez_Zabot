from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.for_questions import get_yes_no_kb

router = Router()  # [1]

@router.message(Command(commands=["start"]))  # [2]
async def cmd_start(message: Message):
    await message.answer("Просто введи: <b>ББВВ</b>\n"
                         f"Например, \n\n <b><i>0619</i></b>\n\n"
                         f"выведет билет <b>06</b>, вопрос <b>19</b>",
                         parse_mode='HTML')

    await message.answer(
        "Нужна видеоинструкция?",
        reply_markup=get_yes_no_kb(),
        parse_mode='HTML'
    )

@router.message(F.text.casefold() == "да")
async def answer_yes(message: Message):
    await message.answer(
        "А нету...",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.casefold() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Ну тогда поехали!",
        reply_markup=ReplyKeyboardRemove()
    )
