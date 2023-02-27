from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from settings import BOT_SOURCE

def bot_source_create_keyboard():
	keyboard = (
		(
			InlineKeyboardButton(
				text = 'The BOT source',
				url = BOT_SOURCE
			),
		),
	)

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup