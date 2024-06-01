from user import User
from datetime import datetime, date
from logger import Logger
from log import Log, LoggingLevel
import json


def main():
    Alexey = User("Alexey", "Agarkov")
    log_of_Alexey = Log(
        date.today(),
        datetime.now(),
        Alexey,
        LoggingLevel.CRITICAL,
        "Brain is damaged")

    Ivan = User("Ivan", "Antsiferov")
    log_of_Ivan = Log(
        date.today(),
        datetime.now(),
        Ivan,
        LoggingLevel.WARNING,
        "Rage is imminent")

    logger = Logger([Ivan])
    logger.accept_event(log_of_Alexey)
    logger.accept_event(log_of_Ivan)
    logger.output_logs()

    print(*logger.retrieve_by_logging_level(LoggingLevel.CRITICAL))

    print(json.dumps(log_of_Ivan, indent=4, sort_keys=True))


main()
