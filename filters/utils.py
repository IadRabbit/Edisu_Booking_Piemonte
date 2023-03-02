from pickle import load
from os.path import exists

from settings import persistence

def exist_chat_id(chat_id: int) -> bool:
	if exists(persistence.filepath):
		with open(persistence.filepath, 'rb') as f:
			c = load(f)

			if chat_id in c['user_data'] and 'token' in c['user_data'][chat_id]:
				return True