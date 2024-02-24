import pytest
from user import User
from datetime import datetime, date
from logger import Logger
from log import Log, LoggingLevel


@pytest.fixture(scope="function")
def users_and_logger() -> None:
    Alexey: User = User("Alexey", "Agarkov")
    log_of_Alexey = Log(
        date.today(),
        datetime.now(),
        Alexey,
        LoggingLevel.CRITICAL,
        "Brain is damaged")

    Ivan = User("Ivan", "Antsiferov")
    log_of_Ivan: Log = Log(
        date.today(),
        datetime.now(),
        Ivan,
        LoggingLevel.WARNING,
        "Rage is imminent")

    Maxim = User("Maxim", "Berezhnoy")
    log_of_Maxim: Log = Log(
        date.today(),
        datetime.now(),
        Maxim,
        LoggingLevel.WARNING,
        "Tinkoff Internship Failed"
    )

    logger = Logger([Ivan, Maxim])
    return [logger, Alexey, log_of_Alexey, Ivan, log_of_Ivan, Maxim, log_of_Maxim]


def test_logs_output_as_a_file(users_and_logger: list) -> None:
    logger: Logger = users_and_logger[0]
    Alexey: User = users_and_logger[1]
    log_of_Alexey: Log = users_and_logger[2]
    Ivan: User = users_and_logger[3]
    log_of_Ivan: Log = users_and_logger[4]
    Maxim: User = users_and_logger[5]
    log_of_Maxim: Log = users_and_logger[6]

    logger.accept_event(log_of_Alexey)
    logger.accept_event(log_of_Ivan)
    logger.accept_event(log_of_Maxim)

    logger.output_logs()

    import os.path
    assert os.path.isfile("logs.txt")

    logs_file = open("logs.txt", mode='r')
    logs_from_file: str = logs_file.read()
    logs_file.close()

    # TODO: do ids have to be verified? ids depend on order in which users have been initialized
    assert "user = Alexey Agarkov, id = 1\nlogging_level = CRITICAL, code = 50\nmessage = Brain is damaged" in logs_from_file
    assert "user = Ivan Antsiferov, id = 2\nlogging_level = WARNING, code = 30\nmessage = Rage is imminent" in logs_from_file
    assert "user = Maxim Berezhnoy, id = 3\nlogging_level = WARNING, code = 30\nmessage = Tinkoff Internship Failed" in logs_from_file
