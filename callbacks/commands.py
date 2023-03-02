from time import sleep
from datetime import datetime

from telegram import Update, InlineQuery
from telegram.ext import ContextTypes, ConversationHandler

from edisu_api import API_SLIM
from edisu_api.geo_utils import parse_location, find_closest

from settings import (
	BOT_NAME, RECV_EMAIL, PASSED_BOOK
)

from inline_keyboards.study_rooms import (
	create_keyboard as study_rooms_create_keyboard,
	create_keyboard_fast as study_room_create_keyboard
)

from inline_keyboards.dates import dates_create_keyboard
from inline_keyboards.signup import signup_create_keyboard
from inline_keyboards.bot_source import bot_source_create_keyboard
from inline_keyboards.delete_booking import delete_booking_create_keyboard
from inline_keyboards.show_bookings import create_keyboard as show_bookings_create_keyboard

from .utils import (
    check_session, check_login, gen_photo_caption
)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if context.user_data.get('token'):
		await update.message.reply_text('Once you start, cannot came back...')

		return ConversationHandler.END

	name = update.effective_user.name

	if not 'token' in context.user_data:
		text = f"Hi {name}, welcome to @{BOT_NAME}, before going on you need to login with your EDISU credentials. In case if you don't have an EDISU account press /signup. If your afraid to use your account read /privacy_disclaimer"
	else:
		text = 'You still need to login. If your afraid to use your account read /privacy_disclaimer'

	await update.message.reply_text(text)

	sleep(1)

	return await login_cmd(update, context)

async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		f"You just gave one more reason to Hanna Baker, congrats :)"
	)

	return ConversationHandler.END

async def login_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		"Send me your EDISU email so we can start."
	)

	return RECV_EMAIL

@check_login
async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	user_info = check_session(edisu_api_user.get_user_info)

	if not user_info:
		return await login_cmd(update, context)

	msg = await update.message.reply_text(
		"Do you have amnesia?"
	)

	sleep(1)

	await msg.edit_text(
		f"Name: {user_info['name']}\n"
		f"Surname: {user_info['surname']}\n"
		f"Email: {user_info['email']}\n"
		f"Matricola: {user_info['studentCode']}"
	)

@check_login
async def get_closest_book_room_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if not 'location' in context.user_data:
		await update.message.reply_text(
			'Maybe you should send me your location baby before I can find the closest book room'
		)

		return

	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	study_rooms_js = check_session(edisu_api_user.get_study_rooms_js_res_mobile, 1)

	if not study_rooms_js:
		return await login_cmd(update, context)

	user_location_coords = context.user_data['location']

	closest, index_study_room = find_closest(
		user_location_coords, edisu_api_user.only_location(study_rooms_js)
	)

	study_room = study_rooms_js['result']['data']['list'][index_study_room]

	await update.message.reply_location(
		latitude = closest['coords']['lat'],
		longitude = closest['coords']['long']
	)

	await update.message.reply_text(
		text = 'Reserve a seat for',
		reply_markup = study_room_create_keyboard(study_room)
	)

@check_login
async def choose_study_room_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	edisu_api_user: API_SLIM = context.chat_data['edisu_session']

	await update.message.reply_text(
		"Okay little Da Vinci, where do we study today?",
		reply_markup = study_rooms_create_keyboard(edisu_api_user)
	)

@check_login
async def show_bookings_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		'Press the button below and press on the booking you wish to see',
		reply_markup = show_bookings_create_keyboard()
	)

async def signup_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		'Press the button below and follow the webpage step until says registration completed & close the page. Then press /login and send me your email & password used in the registration phase',
		reply_markup = signup_create_keyboard()
	)

@check_login
async def set_date_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	text = "Choose the date you prefer"

	if 'last_book_date' in context.user_data:
		date = datetime.strptime(context.user_data['last_book_date'], '%d-%m-%Y')
		text += f"\nCurrently: {date.strftime('%a')} {date.day} {date.strftime('%b')}"

	await update.message.reply_text(
		text,
		reply_markup = dates_create_keyboard()
	)

@check_login
async def get_last_booking_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	last_booking = check_session(edisu_api_user.get_last_booking)

	if not last_booking:
		return await login_cmd(update, context)

	reply_markup = delete_booking_create_keyboard(last_booking['id'])

	if last_booking['booking_status'] in PASSED_BOOK:
		reply_markup = None

	await update.message.reply_photo(
		photo = last_booking['qr_code'],
		caption = gen_photo_caption(last_booking),
		reply_markup = reply_markup
	)

@check_login
async def fast_booking_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if (
		not 'last_study_room' in context.user_data or
		not 'last_id_study_room' in context.user_data or
		not 'last_start_time' in context.user_data or
		not 'last_end_time' in context.user_data
	):
		await update.message.reply_text(
			'First you need to choose a study room, /choose_study_room'
		)

		return

	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	id_study_room = context.user_data['last_id_study_room']
	study_room_location = check_session(edisu_api_user.get_study_room_location, 1, id_study_room)

	if not study_room_location:
		await update.message.reply_text(
			"Couldn't proced with the request, try repeat after /login",
		)
	else:
		date = datetime.today().strftime('%d-%m-%Y')
		study_room = context.user_data['last_study_room']
		last_start_time = context.user_data['last_start_time']
		last_end_time = context.user_data['last_end_time']

		study_room_location = parse_location(study_room_location)

		res = edisu_api_user.pick_random_seat(
			id_study_room, date,
			last_start_time, last_end_time
		)

		msg = res['message'] 

		if msg != 'success':
			await update.message.reply_text(msg)
		else:
			await update.message.reply_text(
				'This is the only way to your graduation'
			)

		last_book = edisu_api_user.get_last_booking()

		await update.message.reply_photo(
			photo = last_book['qr_code'],
			caption = gen_photo_caption(last_book)
		)

		await update.message.reply_location(
			latitude = study_room_location['lat'],
			longitude = study_room_location['long']
		)

@check_login
async def show_study_rooms_location_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	edisu_api_user: API_SLIM = context.chat_data['edisu_session']
	study_rooms_location = check_session(edisu_api_user.get_study_rooms, 1)

	if not study_rooms_location:
		return await login_cmd(update, context)

	for study_room_location in study_rooms_location:
		c_study_room_location = parse_location(study_room_location['location'])

		await update.message.reply_text(
			f"Name: {study_room_location['name']}\n"
			f"Address: {study_room_location['location']}"
		)

		await update.message.reply_location(
			latitude = c_study_room_location['lat'],
			longitude = c_study_room_location['long']
		)

async def feedback_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		'For any questions, problems or features contact @IadRabbit'
	)

async def privacy_disclaimer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		text = (
			f"This bot is an independent project and NOT affiliated in anyway with edisu-piemonte.it\n"
			f"In order to make the bot work properly this is gonna save some personal informations as:\n\n"
			f"1): Your EDISU session, NO email neither password are saved, they are only used temporarily for login step & then retrive the session 'token' used for booking your seats, which means I can access to your edisu booking account\n\n"
			f"2): Other data saved are the last location (if you send me) and last date and time range used for service as /fast_booking or /get_closest_book_room\n\n"
			f"3): If you are truther then you are right I am gonna sell all your data to F.B.I. & Megamind. The bot is completely open source so you can see by yourself what it does. More details here /bot_source_info"
		)
	)

async def bot_source_info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		text = (
			f"This bot is developed by wrapping API endpoints calls by monitoring network traffic from the web version & sniffing the calls for the mobile app.\n"
			f"The bot source can be found pressing the button below"
		),
		reply_markup = bot_source_create_keyboard()
	)

async def cmds_list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
	text = 'The bot commands are the following:\n\n'

	for a in range(L_CMDS):
		text += f"{a + 1}:) /{cmds[a][0]} - {cmds[a][2]}\n\n"

	await update.message.reply_text(
		text = text
	)

cmds = (
	(
		'fast_booking', fast_booking_cmd, 'Make a booking using the last time range, userful for making a booking during the next day at the same hours'
	),
	(
		'get_last_booking', get_last_booking_cmd, 'Get your last booking'
	),
	(
		'choose_study_room', choose_study_room_cmd, 'Select in which study room you prefer to study'
	),
	(
		'get_closest_book_room', get_closest_book_room_cmd, 'Receive the study room location nearest to you'
	),
	(
		'show_bookings', show_bookings_cmd, f'Receive your bookings list (limited to the last {InlineQuery.MAX_RESULTS} due telegram limitation)'
	),
	(
		'set_date', set_date_cmd, 'Change the date of the booking. (DEFAULT DATE: today)'
	),
	(
		'show_study_rooms_location', show_study_rooms_location_cmd, 'Get the location of all study rooms'
	),
	(
		'info', info_cmd, 'Get your EDISU profile infos'
	),
	(
		'cmds_list', cmds_list_cmd, 'Get the list of all commands for this bot'
	),
	(
		'feedback', feedback_cmd, 'It will send you an unicorn'
	),
	(
		'privacy_disclaimer', privacy_disclaimer_cmd, 'Some infos about the privacy'
	),
	(
		'bot_source_info', bot_source_info_cmd, 'Some infos on the bot code'
	),
	(
		'signup', signup_cmd, 'Create an EDISU profile if you don\'t have one'
	)
)

L_CMDS = len(cmds)