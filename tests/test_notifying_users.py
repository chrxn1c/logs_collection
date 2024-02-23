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


def test_notifying_users(users_and_logger: list, capsys) -> None:
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

    for message_number in range(9):
        new_log: Log = Log(
            date.today(),
            datetime.now(),
            Maxim,
            LoggingLevel.WARNING,
            "message number " + str(message_number))

        logger.accept_event(new_log)

    captured_message = capsys.readouterr()
    assert captured_message.out == f"""User {Maxim.get_full_name()} now has {
        10} errors!\n"""
