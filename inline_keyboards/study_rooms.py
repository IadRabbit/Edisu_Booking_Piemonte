from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from edisu_api import API_SLIM

def create_keyboard(edisu_api_user: API_SLIM):
	study_rooms = edisu_api_user.get_study_rooms(1)

	keyboard = [
		[
			InlineKeyboardButton(
				text = study_room['name'],
				callback_data = f"/study_room_{study_room['id']}"
			)
			for study_room in study_rooms[a:a+2]
		]
		for a in range(0, len(study_rooms), 2)
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup

def create_keyboard_fast(study_room: dict):
	keyboard = (
		(
			InlineKeyboardButton(
				text = study_room['name'],
				callback_data = f"/study_room_{study_room['id']}"
			),
		),
	)

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup