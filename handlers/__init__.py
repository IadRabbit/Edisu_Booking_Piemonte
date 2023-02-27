from .commands import handlers as commands_handlers
from .messages import handlers as messages_handlers
from .inlines_query import handlers as inlines_handlers
from .callbacks_query import handlers as callbacks_handlers
from .conversations import handlers as conversations_handlers

handlers = ()
handlers += conversations_handlers
handlers += messages_handlers
handlers += commands_handlers
handlers += callbacks_handlers
handlers += inlines_handlers