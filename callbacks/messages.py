from time import sleep

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from edisu_api.api_slim import API_SLIM
from edisu_api.exceptions import CannotLogin

from settings import RECV_PASSWORD, PASSED_BOOK
from inline_keyboards.delete_booking import delete_booking_create_keyboard, ask_confirm_delete_booking_create_keyboard

from .commands import get_closest_book_room_cmd, login_cmd

from .utils import (
    check_login, check_session, gen_photo_caption
)

async def first_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		"It is your first time isn't it?.\nPress /start if you want to visit the Deep Rabbit's Hole or /signup if you haven't created an EDISU account"
	)

async def recv_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.chat_data['email'] = update.effective_message.text

	await update.message.reply_text(
		"Okay, now gimme your password so I can hack you :)"
	)

	return RECV_PASSWORD

async def recv_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
	password = update.effective_message.text
	email = context.chat_data['email']

	edisu_api_user = API_SLIM()

	try:
		edisu_api_user.login(email, password)
		context.user_data['token'] = edisu_api_user.jwt_token

		if 'edisu_session' in context.chat_data:
			del context.chat_data['edisu_session']
		
		text = f'You are in. No excape from study no more'
	except CannotLogin as err:
		text = f'{err.msg}\nTry login again sending email & password. As describerd in /login'

	await update.message.reply_text(text)

	return ConversationHandler.END

async def recv_user_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
	user_location = update.effective_message.location

	context.user_data['location'] = {
		'lat': user_location.latitude,
		'long': user_location.longitude
	}

	await update.message.reply_text(
		"Thanks F.B.I. is coming to your house. RUN..."
	)

	sleep(1)

	await update.message.reply_text(
		"I am kidding, don't worry (or maybe not...)"
	)

	await get_closest_book_room_cmd(update, context)

@check_login
async def info_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
	id_booking = int(
		update.message.text.removeprefix('#info_booking_')
	)

	await update.message.delete()
	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	booking = check_session(edisu_api_user.get_user_booking, id_booking)

	if not booking:
		return await login_cmd(update, context)

	reply_markup = delete_booking_create_keyboard(id_booking)

	if booking['booking_status'] in PASSED_BOOK:
		reply_markup = None

	await update.message.reply_photo(
		photo = booking['qr_code'],
		caption = gen_photo_caption(booking),
		reply_markup = reply_markup
	)