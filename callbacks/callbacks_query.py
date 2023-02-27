from datetime import datetime
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from edisu_api.api_slim import API_SLIM
from edisu_api.geo_utils import parse_location

from inline_keyboards.slots_time import (
    create_keyboard_start_time,
    create_keyboard_end_time
)

from inline_keyboards.dates import dates_create_keyboard

from inline_keyboards.delete_booking import (
    ask_confirm_delete_booking_create_keyboard,
    delete_booking_create_keyboard
)

from settings import (
	RECV_STUDY_ROOM_TIME_START, RECV_STUDY_ROOM_TIME_END, RECV_DEL_BOOK_CONFIRM
)

from .utils import (
    check_login, check_session, gen_photo_caption
)

@check_login
async def choose_time_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	study_room_data = update.callback_query.data

	buttons: tuple[
		tuple[
			InlineKeyboardButton
		]
	] = update.callback_query.message.reply_markup.inline_keyboard
	
	for row in buttons:
		for button in row:
			if button.callback_data == study_room_data:
				study_room = button.text
				break

	id_study_room = int(
		study_room_data.removeprefix('/study_room_')
	)

	context.user_data['last_id_study_room'] = id_study_room
	context.user_data['last_study_room'] = study_room

	reply_markup = create_keyboard_start_time(
		study_room, id_study_room,
		context.user_data, context.chat_data['edisu_session']
	)

	if not reply_markup:
		await update.callback_query.answer(
			text = f"The study room {study_room} could be closed on {context.user_data['last_book_date']}",
			show_alert = True
		)

		return ConversationHandler.END

	await update.callback_query.edit_message_text(
		text = 'Ok you lazy, when you want to start your way to breakdown :)',
		reply_markup = reply_markup
	)

	return RECV_STUDY_ROOM_TIME_START

async def choose_time_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
	index_time_slot_chosen = int(
		update.callback_query.data.removeprefix('/time_')
	)

	last_time_slots = context.user_data['last_time_slots']
	context.user_data['last_start_time'] = last_time_slots[index_time_slot_chosen]
	context.user_data['last_time_slots'] = last_time_slots[index_time_slot_chosen + 1:]
	last_time_slots = context.user_data['last_time_slots']

	await update.callback_query.edit_message_text(
		text = 'Nice, now select when finish your agony :)',
		reply_markup = create_keyboard_end_time(last_time_slots)
	)

	return RECV_STUDY_ROOM_TIME_END

@check_login
async def reserve_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.callback_query.edit_message_text("Let's see if you can run from study...")

	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	id_study_room = context.user_data['last_id_study_room']
	study_room_location = check_session(edisu_api_user.get_study_room_location, 1, id_study_room)

	if not study_room_location:
		await update.callback_query.answer(
			"Couldn't proced with the request, try repeat after /login",
			show_alert = True
		)
	else:
		date = context.user_data['last_book_date']
		study_room = context.user_data['last_study_room']
		last_start_time = context.user_data['last_start_time']

		index_time_slot_chosen = int(
			update.callback_query.data.removeprefix('/time_')
		)

		last_end_time = context.user_data['last_time_slots'][index_time_slot_chosen]
		context.user_data['last_end_time'] = last_end_time

		study_room_location = parse_location(study_room_location)

		res = edisu_api_user.pick_random_seat(
			id_study_room, date, 
			last_start_time, last_end_time
		)

		if not res:
			await update.callback_query.answer("Couldn't find any slot", show_alert = True)
			return

		msg = res['message'] 

		if msg != 'success':
			await update.callback_query.answer(msg, show_alert = True)
		else:
			await update.callback_query.answer(
				'This is the only way to your graduation'
			)

		last_book = edisu_api_user.get_last_booking()

		chat_id = update.callback_query.message.chat_id

		await context.bot.send_photo(
			chat_id = chat_id,
			photo = last_book['qr_code'],
			caption = gen_photo_caption(last_book)
		)

		await context.bot.send_location(
			chat_id = chat_id,
			latitude = study_room_location['lat'],
			longitude = study_room_location['long']
		)

		await update.callback_query.delete_message()

	return ConversationHandler.END

async def ask_book_del_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
	id_booking = int(
		update.callback_query.data.removeprefix('/del_booking_')
	)

	await update.callback_query.edit_message_caption(
		caption = 'Are you sure ?',
		reply_markup = ask_confirm_delete_booking_create_keyboard(id_booking)
	)	

	return RECV_DEL_BOOK_CONFIRM

@check_login
async def del_booking_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
	edisu_api_user: API_SLIM = context.chat_data['edisu_session']

	id_booking = int(
		update.callback_query.data.removeprefix('/del_booking_yes_')
	)

	del_booking = check_session(edisu_api_user.book_cancel_js_res, id_booking)

	if not del_booking:
		text = "Couldn't proced with the request, try repeat after /login"
	else:
		text = f"The booking {id_booking} has been deleted"

	await update.callback_query.answer(
		text = text,
		show_alert = True
	)

	await update.callback_query.delete_message()

	return ConversationHandler.END

async def del_booking_no(update: Update, context: ContextTypes.DEFAULT_TYPE):
	id_booking = int(
		update.callback_query.data.removeprefix('/del_booking_no_')
	)

	await update.callback_query.answer("I deleted it anyway :))... Kidding")

	await update.callback_query.edit_message_reply_markup(
		delete_booking_create_keyboard(id_booking)
	)

	return ConversationHandler.END

async def set_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
	date_unix = float(
		update.callback_query.data.removeprefix('/set_date_')
	)

	c_date = datetime.fromtimestamp(date_unix)
	context.user_data['last_book_date'] = c_date.strftime('%d-%m-%Y')

	text = f"Choose the date you prefer\nCurrently: {c_date.strftime('%a')} {c_date.day} {c_date.strftime('%b')}"

	await update.callback_query.message.edit_text(
		text = text,
		reply_markup = dates_create_keyboard()
	)

	await update.callback_query.answer(f"Date set to {context.user_data['last_book_date']}")