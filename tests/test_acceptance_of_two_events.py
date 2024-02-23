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


def test_acceptance_of_two_events(users_and_logger: list) -> None:
    logger: Logger = users_and_logger[0]
    Alexey: User = users_and_logger[1]
    log_of_Alexey: Log = users_and_logger[2]
    Ivan: User = users_and_logger[3]
    log_of_Ivan: Log = users_and_logger[4]
    Maxim: User = users_and_logger[5]
    log_of_Maxim: Log = users_and_logger[6]

    logger.accept_event(log_of_Alexey)
    logger.accept_event(log_of_Ivan)

    assert log_of_Alexey in logger._logs
    assert log_of_Ivan in logger._logs
    assert log_of_Maxim not in logger._logs
