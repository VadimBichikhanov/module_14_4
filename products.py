from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import logging
from os import path
from crud_functions import get_all_products

# Список продуктов с изображениями
products_with_images = [
    {"name": "Apple", "description": "Свежее яблоко", "price": 100, "image": "images/apple.jpg"},
    {"name": "Banana", "description": "Спелый банан", "price": 200, "image": "images/banana.jpg"},
    {"name": "Orange", "description": "Апельсин", "price": 300, "image": "images/orange.jpg"},
    {"name": "Grapes", "description": "Виноград", "price": 400, "image": "images/grapes.jpg"}
]

async def get_buying_list(message: Message):
    products = get_all_products()

    for product in products:
        _, title, description, price, image = product
        await message.answer(f"Название: {title} | Описание: {description} | Цена: {price}")
        
        # Отправка изображения для продукта
        if image and path.exists(image):
            logging.info(f"Отправка изображения: {image}")
            await message.answer_photo(photo=FSInputFile(path=image))
        else:
            logging.error(f"Изображение для продукта {title} не найдено.")
            await message.answer(f"Изображение для продукта {title} не найдено.")

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Apple", callback_data="buy_apple")],
            [InlineKeyboardButton(text="Banana", callback_data="buy_banana")],
            [InlineKeyboardButton(text="Orange", callback_data="buy_orange")],
            [InlineKeyboardButton(text="Grapes", callback_data="buy_grapes")]
        ]
    )
    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)