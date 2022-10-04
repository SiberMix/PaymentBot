import logging

import aiogram
import config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
disp = Dispatcher(bot)
price = types.LabeledPrice(label="Подписка на курс по Python", amount=500 * 100)


@disp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if config.PAY_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, f"Платеж на сумму {price.amount / 100} для оплаты подписки")
    await bot.send_invoice(message.chat.id, title='Подписка на курс по Python',
                           description='Активация подписки на курс', provider_token=config.PAY_TOKEN, currency="rub",
                           photo_url='https://fs.znanio.ru/3513d2/8d/29/b1a2eb318c4fd5b85df2c5dd2a8b93bed6.png',
                           photo_width=416, photo_height=234, photo_size=416, is_flexible=False, prices=[price],
                           start_parameter='one-month-subscription',
                           payload='test-invoice-payload')


@disp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query_query(pre_checkhout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkhout_q.id, ok=True)


@disp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v} ")
        await bot.send_message(message.chat.id, 'Платеж за курс успешно оплачен!')


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=False)
