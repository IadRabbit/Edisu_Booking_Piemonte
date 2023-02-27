from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from settings import MAX_DAYS

def dates_create_keyboard():
	dates = [
		datetime.today() + timedelta(days = a)
		for a in range(MAX_DAYS + 1)
	]

	keyboard = [
		[
			InlineKeyboardButton(
				text = f"{date.strftime('%a')} {date.day} {date.strftime('%b')}",
				callback_data = f'/set_date_{date.timestamp()}'
			)
			for date in dates[a:a+3]
		]
		for a in range(0, len(dates), 3)
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup