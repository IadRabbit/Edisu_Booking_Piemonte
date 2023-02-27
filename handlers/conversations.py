from telegram.ext import (
	ConversationHandler, CommandHandler, MessageHandler
)

from telegram.ext.filters import TEXT, COMMAND

from callbacks.commands import (
	start_cmd, login_cmd, cancel_cmd
)

from callbacks.messages import recv_email, recv_password

from settings import RECV_EMAIL, RECV_PASSWORD

start_cmd_handler = CommandHandler('start', start_cmd)
login_cmd_handler = CommandHandler('login', login_cmd)

login_conv_handler = ConversationHandler(
	entry_points = (
		start_cmd_handler, login_cmd_handler
	),
	states = {
		RECV_EMAIL: (
			MessageHandler(
				filters = TEXT & ~COMMAND,
				callback = recv_email
			),
		),
		RECV_PASSWORD: (
			MessageHandler(
				filters = TEXT & ~COMMAND,
				callback = recv_password
			),
		)
	},
	fallbacks = (
		start_cmd_handler, login_cmd_handler,
		CommandHandler('cancel', cancel_cmd)
	),
)

handlers = (
	login_conv_handler,
)