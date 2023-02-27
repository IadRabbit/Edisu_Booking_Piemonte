from telegram.ext import ContextTypes

from telegram import (
    Update, InlineQueryResultGif, InlineQuery,
	InlineQueryResultArticle, InputTextMessageContent
)

from edisu_api import API_SLIM

from settings import STATUS_BOOKING

from .utils import check_session

async def show_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
	edisu_api_user = API_SLIM()
	token = context.user_data['token']
	edisu_api_user.set_token(token)

	list_bookings = check_session(edisu_api_user.get_booking_list)

	if not list_bookings:
		result = [
			InlineQueryResultGif(
				id = 'not_found',
				gif_url = 'https://i.giphy.com/media/8L0Pky6C83SzkzU55a/200w.gif',
				thumb_url= 'https://i.giphy.com/media/8L0Pky6C83SzkzU55a/200w.gif'
			)
		]
	else:
		result = [
			InlineQueryResultArticle(
				id = booking['booking_id'],
				title = f"Booking ID: {booking['booking_id']}",
				thumb_url = booking['qr_code'],
				input_message_content = InputTextMessageContent(
					f"#info_booking_{booking['id']}"
				),
				description = (
					f"Status: {STATUS_BOOKING[booking['booking_status']]}\n"
					f"Booking Date: {booking['date']}\n"
					f"Range Time: {booking['start_time']} - {booking['end_time']}"
					#f"Study Room: {booking['hall_name']}"
					#f"Seay No: {booking['seat_no']}"
				)
			)
			for booking in list_bookings[:InlineQuery.MAX_RESULTS]
		]

	await update.inline_query.answer(result)