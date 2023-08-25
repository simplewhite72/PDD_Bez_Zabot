from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from configs import config

admin_buttons = ["Добавить видео", "Протестировать вопрос", "Перезагрузка бота", "Удалить видео"]

def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=admin_buttons[1])
    kb.button(text=admin_buttons[2])
    kb.button(text=admin_buttons[0])
    kb.button(text=admin_buttons[3])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def admin_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="/root")
    return kb.as_markup(resize_keyboard=True)

def inline_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()  
    kb.button(text="Посмотреть еще видео", url=config.bot_link+"?start=start")
    kb.button(text="Купить автору кофе", url=config.donate_link)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def donate_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()  
    kb.button(text="Купить автору кофе", url=config.donate_link)
    return kb.as_markup(resize_keyboard=True)

