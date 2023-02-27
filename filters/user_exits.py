from telegram import Message
from telegram.ext.filters import MessageFilter

from .utils import exist_chat_id

permitted_cmds = {
	'/signup', '/bot_source_info',
	'/privacy_disclaimer', '/feedback', '/cmds_list'
}

class UserExistsBack(MessageFilter):
	def filter(self, msg: Message):
		chat_id = msg.chat_id

		if msg.text in permitted_cmds:
			return False

		return not exist_chat_id(chat_id)