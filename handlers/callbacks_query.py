from telegram.ext import CallbackQueryHandler, ConversationHandler

from callbacks.callbacks_query import (
	choose_time_start, choose_time_end, reserve_booking,
    ask_book_del_confirm, del_booking_yes, del_booking_no,
    set_date
)

from settings import (
    RECV_STUDY_ROOM_TIME_START, RECV_STUDY_ROOM_TIME_END,
    RECV_DEL_BOOK_CONFIRM
)

book_seat_conv_handler = ConversationHandler(
	per_message = True,
	entry_points = (
		CallbackQueryHandler(
			callback = choose_time_start,
			pattern = '^(/study_room_)'
		),
	),
	states = {
		RECV_STUDY_ROOM_TIME_START: (
			CallbackQueryHandler(
				callback = choose_time_end,
				pattern = '^(/time_)'
			),
		),
		RECV_STUDY_ROOM_TIME_END: (
			CallbackQueryHandler(
				callback = reserve_booking,
				pattern = '^(/time_)'
			),
		)
	},
	fallbacks = (),
)

del_book_conv_handler = ConversationHandler(
	per_message = True,
	entry_points = (
		CallbackQueryHandler(
			callback = ask_book_del_confirm,
			pattern = '^(/del_booking_)'
		),
	),
	states = {
		RECV_DEL_BOOK_CONFIRM: (
			CallbackQueryHandler(
				callback = del_booking_yes,
				pattern = '^(/del_booking_yes_)'
			),
		),
	},
	fallbacks = (
		CallbackQueryHandler(
			callback = del_booking_no,
			pattern = '^(/del_booking_no_)'
		),
	),
)

set_date_handler = CallbackQueryHandler(
	callback = set_date,
	pattern = '^(/set_date_)'
)

handlers = (
	book_seat_conv_handler,
    del_book_conv_handler,
    set_date_handler
)