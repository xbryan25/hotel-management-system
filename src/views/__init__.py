
from .pages import *
from .message_dialogs import *
from .data_dialogs import *

__all__ = (
    __import__('views.pages').pages.__all__ +
    __import__('views.data_dialogs').data_dialogs.__all__ +
    __import__('views.message_dialogs').message_dialogs.__all__
)
