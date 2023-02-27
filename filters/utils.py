from pickle import load
from os.path import exists

from settings import BOT_NAME

def exist_chat_id(chat_id: int) -> bool:
	if exists(f'{BOT_NAME}.db'):
		with open(f'{BOT_NAME}.db', 'rb') as f:
			c = load(f)

			if chat_id in c['user_data'] and 'token' in c['user_data'][chat_id]:
				return True