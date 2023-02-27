from telegram.ext import (
    ApplicationBuilder, PicklePersistence, PersistenceInput
)

import log
from handlers import handlers
from settings import BOT_TOKEN, BOT_NAME

if __name__ == '__main__':
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

	application = (
		ApplicationBuilder()
		.token(BOT_TOKEN)
		.persistence(persistence)
		.build()
	)

	application.add_handlers(handlers)
	application.run_polling()