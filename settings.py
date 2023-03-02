from telegram.ext import PicklePersistence, PersistenceInput

BOT_TOKEN = 'BOT_TOKEN'
BOT_NAME = 'Edisu_Booking_Piemonte_bot'.lower()

persistence = PicklePersistence(
	filepath = f'{BOT_NAME}.db',
	store_data = PersistenceInput(
		user_data = True,
		chat_data = False,
		bot_data = False,
		callback_data = False
	),
	update_interval = 2
)

MAX_DAYS = 7

RECV_EMAIL, RECV_PASSWORD = range(2)
RECV_STUDY_ROOM_TIME_START, RECV_STUDY_ROOM_TIME_END = range(2)
RECV_DEL_BOOK_CONFIRM = range(1)
PASSED_BOOK = (0,)

STATUS_BOOKING = {
	0: 'Canceled',
	1: 'Upcoming',
	2: 'Completed',
	4: 'Pending'
}

BOT_SOURCE = 'https://github.com/IadRabbit/Edisu_Booking_Piemonte'