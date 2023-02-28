from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from edisu_api import API_SLIM
from edisu_api.exceptions import PossibleClosedStudyRoom

def __create_keyboard(time_slots: list[str]):
	keyboard = [
		[
			InlineKeyboardButton(
				text = time_slot,
				callback_data = f"/time_{time_slots.index(time_slot)}"
			)
			for time_slot in time_slots[a:a+3]
		]
		for a in range(0, len(time_slots), 3)
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup

def create_keyboard_start_time(
	study_room: str,
	id_study_room: int,
	user_data: dict,
	edisu_api_user: API_SLIM
):
	try:
		time_slots = edisu_api_user.get_time_slots(
			study_room, id_study_room, user_data['last_book_date']
		)
	except PossibleClosedStudyRoom:
		return

	user_data['last_time_slots'] = time_slots

	return __create_keyboard(time_slots[:-1])

def create_keyboard_end_time(
	time_slots = list[str],
):
	return __create_keyboard(time_slots)