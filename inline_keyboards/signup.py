from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

def signup_create_keyboard():
	keyboard = (
		(
			InlineKeyboardButton(
				text = 'Signup',
				web_app = WebAppInfo('https://edisuprenotazioni.edisu-piemonte.it/auth/register')
			),
		),
	)

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup