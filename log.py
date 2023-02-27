from settings import BOT_NAME
from logging import basicConfig, INFO

basicConfig(
	format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level = INFO,
	filename = f'{BOT_NAME}.log'
)