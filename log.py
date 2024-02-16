from datetime import datetime, date
from user import User
from enum import Enum
import logging
# log: [date, time, user, logging_level, message]


class LoggingLevel(Enum):
    NOT_SET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __str__(self) -> str:
        return f"{str(self.name)}, code = {str(self.value)}"

# TODO: add message to Log


class Log:
    def __init__(self, date: date, time: datetime, user: User, logging_level: LoggingLevel, message: str) -> None:
        self.date: datetime.date = date
        self.time: datetime.time = time
        self.user: User = user
        self.logging_level: LoggingLevel = logging_level
        self.message: str = message

    def __str__(self) -> str:
        return f"date = {str(self.date)}\ntime = {str(self.time)}\nuser = {str(self.user)}\nlogging_level = {str(self.logging_level)}\nmessage = {self.message}\n"
