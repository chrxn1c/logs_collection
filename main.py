
# capture logs from system by some parameter

# user can be tracked. every 10th error of the tracked users is reported.

# output all logs as a file


from user import User
from datetime import datetime, date
from logger import Logger, logs
from log import Log, LoggingLevel


def main():
    Alexey = User("Alexey", "Agarkov", 1)
    log_of_Alexey = Log(
        date.today(),
        datetime.now(),
        Alexey,
        LoggingLevel.CRITICAL,
        "Brain is damaged")

    Ivan = User("Ivan", "Antsiferov", 2)
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


main()
