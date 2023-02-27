from telegram.ext import CommandHandler

from callbacks.commands import cmds

handlers = tuple(
	[
		CommandHandler(cmd_data[0], cmd_data[1])
		for cmd_data in cmds
	]
)