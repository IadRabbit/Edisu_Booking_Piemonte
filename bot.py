from telegram.ext import ApplicationBuilder

import log
from handlers import handlers
from settings import BOT_TOKEN, persistence

if __name__ == '__main__':
	application = (
		ApplicationBuilder()
		.token(BOT_TOKEN)
		.persistence(persistence)
		.build()
	)

	application.add_handlers(handlers)
	application.run_polling()