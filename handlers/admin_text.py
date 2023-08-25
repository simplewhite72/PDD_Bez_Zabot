from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from functions import save_stat, write_questions
from configs import config
from typing import Dict
from keyboards.for_questions import admin_kb, admin_buttons, admin_cancel
from filters.admin import AdminTypeFilter
from filters.question import QuestionTypeFilter
import datetime
import os, signal

class Admin_Mode(StatesGroup):
    choosing_mode = State()
    choosing_question = State()
    adding_video = State()
    adding_video_questions = State()
    adding_video_title = State()
    deleting_video = State()
    deleting_video_questions = State()

router = Router()
router.message.filter(
                    AdminTypeFilter(user_id=config.admin_id) # Фильтр на админа по айди
                    )
# Инициализация по команде
@router.message(Command("root"))
async def message_with_text(message: Message, state:FSMContext):
    await message.answer('Добро пожаловать в управление ботом',
                         reply_markup=admin_kb(),
                         parse_mode='HTML'
                        )
    await state.set_state(Admin_Mode.choosing_mode)

#///////////////////////////////////////////////////////////     ПЕРЕЗУГРУЗКА БОТА     ///////////////////////////////////////////////////////////////////////
# Перезагрузка бота
@router.message(Admin_Mode.choosing_mode, F.text == admin_buttons[2])
async def test_entering(message: Message, state: FSMContext):
    
    #await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Перезагружаюсь...",
        reply_markup=admin_cancel()
    )
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

#///////////////////////////////////////////////////////////     ТЕСТИРОВАНИЕ БИЛЕТОВ     ///////////////////////////////////////////////////////////////////////
# Состояние выбора режима. Выбирается режим тестирования билетов
@router.message(Admin_Mode.choosing_mode, F.text == admin_buttons[1])
async def test_entering(message: Message, state: FSMContext):
    
    #await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Пиши вопрос тогда, хули...",
        reply_markup=admin_cancel()
    )
    await state.set_state(Admin_Mode.choosing_question)

# Режим тестирования билетов. Перехват правильного вопроса
@router.message(Admin_Mode.choosing_question, F.text, QuestionTypeFilter(str(F.Text),config.output_df))
async def test_questions(message: Message, output: Dict[str, str], state: FSMContext):
    s = output['video_file_id']
    username = str(message.from_user.username)
    first_name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    user_id = str(message.from_user.id)
    cap = "<b>"+output['title']+"</b>" + "\n\n"+ output['caption'] + "\n\n" + u'\U00002705' +config.LINK_1 + "\n" +  u'\U00002705' + config.LINK_2
    dt = datetime.datetime.now()
    now_time = dt.strftime('%H:%M:%S')
    now_date = dt.strftime('%m.%d.%Y')
    response = (now_date,now_time,user_id,username,first_name,last_name,int(message.text[0:2]),int(message.text[2:4]))
    save_stat.write_to_stat(response)
    if s == 'None' :
        await message.answer('Запрошенный вопрос еще не появился...',
                             reply_markup=admin_cancel()) 
    else :
        await message.answer_video(video=s, 
                                   width=1920, 
                                   height=1080, 
                                   caption=cap, 
                                   supports_streaming=True,
                                   reply_markup=admin_cancel(),
                                   parse_mode='HTML'
                                   )
# Обработка сообщений, не прошедших прошлый фильтр на ББВВ
@router.message(Admin_Mode.choosing_question, F.text)
async def test_questions(message: Message, state: FSMContext):
    await message.answer('Введите вопрос в формате ББВВ, пожалуйста',
                            reply_markup=admin_cancel()) 


#///////////////////////////////////////////////////////////     ДОБАВЛЕНИЕ ВИДЕО     ///////////////////////////////////////////////////////////////////////
# Перевод на режим добавления видео
@router.message(Admin_Mode.choosing_mode, F.text == admin_buttons[0])
async def video_upload_entering(message: Message, state: FSMContext):
    await message.answer(
        text="Жду видео тогда, хули...",
        reply_markup=admin_cancel()
    )
    await state.set_state(Admin_Mode.adding_video)    

# Ловим видео    
@router.message(Admin_Mode.adding_video, F.video)
async def upload_video(message: Message, state: FSMContext):
    await state.update_data(file_id=message.video.file_id)
    await message.answer(
        text="Видео получено. Теперь напиши вопросы в формате ББВВ ББВВ ББВВ",
        reply_markup=admin_cancel()
    )
    await state.set_state(Admin_Mode.adding_video_questions)    

# Ловим строку с вопросами
@router.message(Admin_Mode.adding_video_questions, F.text)
async def upload_video_questions(message: Message, state: FSMContext):
    await state.update_data(questions=message.text)
    await message.answer(
        text="Получено. Теперь напиши описание!",
        reply_markup=admin_cancel()
    )
    await state.set_state(Admin_Mode.adding_video_title)         

# Ловим описание видео и пишем в базу данных. Сбрасываем конечный автомат
@router.message(Admin_Mode.adding_video_title, F.text)
async def upload_video_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    user_data = await state.get_data()
    write_questions.write_question_to_db(user_data['file_id'], user_data['questions'], user_data['title'])
    await message.answer(
        text=f"Вы загрузили видео {user_data['file_id']}.\n"
             f"Вы выбрали вопросы {user_data['questions']}.\n"
             f"Описание вопросов: {user_data['title']}.\n"
             f"Перезагружаюсь...",
        reply_markup=admin_cancel()
    )
    await state.clear()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)


#///////////////////////////////////////////////////////////     УДАЛЕНИЕ ВИДЕО     ///////////////////////////////////////////////////////////////////////
# Удаление видео. Запрашиваем строку с вопросами
@router.message(Admin_Mode.choosing_mode, F.text == admin_buttons[3])
async def test_entering(message: Message, state: FSMContext):
    await message.answer(
        text="Какие вопросы удаляем? (ББВВ ББВВ ББВВ)",
        reply_markup=admin_cancel()
    )
    await state.set_state(Admin_Mode.deleting_video)

# Удаление видео. Пишем в базу данных.
@router.message(Admin_Mode.deleting_video, F.text)
async def test_entering(message: Message, state: FSMContext):
    await state.update_data(questions_to_delete=message.text)
    user_data = await state.get_data()
    write_questions.delete_question_from_db(user_data['questions_to_delete'])
    await message.answer(
        text=f"Вы выбрали вопросы {user_data['questions_to_delete']}.\n"
             f"Перезагружаюсь...",
        reply_markup=admin_cancel()
    )
    await state.clear()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)