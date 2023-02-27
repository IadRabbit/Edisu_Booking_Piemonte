from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard():
	keyboard = [
		[
			InlineKeyboardButton(
				text = 'See your bookings',
				switch_inline_query_current_chat = f'/show_bookings{uuid4()}'
			)
		]
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup