from types import NoneType
from telegram import Update
from telegram.ext import ContextTypes

from edisu_api.api_slim import API_SLIM

from settings import STATUS_BOOKING

def check_session(func, *args) -> NoneType | dict:
	try:
		return func(*args)
	except:
		return
	
def check_login(function):
	def wrap(update: Update, context: ContextTypes.DEFAULT_TYPE):
		if not 'edisu_session' in context.user_data:
			edisu_api_user = API_SLIM()
			token = context.user_data['token']
			edisu_api_user.set_token(token)
			context.chat_data['edisu_session'] = edisu_api_user

		return function(update, context)

	return wrap

def gen_photo_caption(booking: dict):
	caption = (
		f"Booking ID: {booking['booking_id']}\n"
		f"Status: {STATUS_BOOKING[booking['booking_status']]}\n"
		f"Seat No: {booking['seat_no']}\n"
		f"Date: {booking['date']}\n"
		f"Study Room: {booking['hall_name']}\n"
		f"Floor No: {booking['floor_no']}\n"
		f"Start Time: {booking['start_time']}\n"
		f"End Time: {booking['end_time']}\n"
	)

	return caption