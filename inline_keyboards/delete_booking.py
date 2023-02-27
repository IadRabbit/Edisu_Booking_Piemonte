from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def delete_booking_create_keyboard(id_booking: int):
	keyboard = (
		(
			InlineKeyboardButton(
				text = 'Delete This Booking',
				callback_data = f'/del_booking_{id_booking}'
			),
		),
	)

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup

def ask_confirm_delete_booking_create_keyboard(id_booking: int):
	keyboard = (
		(
			InlineKeyboardButton(
				text = 'Yes',
				callback_data = f'/del_booking_yes_{id_booking}'
			),
			InlineKeyboardButton(
				text = 'No',
				callback_data = f'/del_booking_no_{id_booking}'
			)
		),
	)

	reply_markup = InlineKeyboardMarkup(keyboard)

	return reply_markup