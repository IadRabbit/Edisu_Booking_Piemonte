from telegram.ext.filters import LOCATION, Regex
from telegram.ext import MessageHandler

from callbacks.messages import (
    first_time, recv_user_location, info_booking
)

from filters.user_exits import UserExistsBack

msg_location_handler = MessageHandler(
    filters = LOCATION,
    callback = recv_user_location
)

first_time_handler = MessageHandler(
	filters = UserExistsBack(),
	callback = first_time
)

info_booking_handler = MessageHandler(
    filters = Regex('^(#info_booking_)'),
    callback = info_booking
)

handlers = (
	first_time_handler,
	msg_location_handler,
    info_booking_handler
)