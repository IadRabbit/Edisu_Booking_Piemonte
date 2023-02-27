from telegram.ext import InlineQueryHandler

from callbacks.inlines_query import show_bookings

conv_handler = InlineQueryHandler(
	callback = show_bookings,
	pattern = '^(/show_booking)'
)

handlers = (
	conv_handler,
)