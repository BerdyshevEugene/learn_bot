import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext, CallbackQueryHandler)
from translate import Translator


logger = logging.getLogger(__name__)
language = ""

def select_language(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton('English', callback_data='English'),
            InlineKeyboardButton('Spanish', callback_data='Spanish'),
            InlineKeyboardButton('Russian', callback_data='Russian'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose language!', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    global language
    language = update.callback_query.data.lower()
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f'{query.data} has been selected for'
                            'translation. Enter your text.')


def language_translator(user_input):
    translator = Translator(from_lang="russian", to_lang=language)
    translation = translator.translate(user_input)
    return translation


def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(language_translator(user_input))


def main():
    api = open("api.txt", "r")
    updater = Updater(api.read(), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', select_language))
    dp.add_handler(CommandHandler('select_language', select_language))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='main.log',
        filemode='w',
        level=logging.DEBUG
    )
 
    main()
