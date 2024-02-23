from log import Log, LoggingLevel
from user import User

logs: list[Log] = []


# TODO: add tracking of user

class Logger:
    def __init__(self, trackable_users: list[User]) -> None:
        self.tracked_users: list[User] = trackable_users.copy()

    def track_new_users(self, new_tracked_users: list[User]) -> None:
        for now_tracked_user in new_tracked_users:
            self.tracked_users.append(now_tracked_user)

    def accept_event(self, log: Log) -> None:
        logs.append(log)

    def retrieve_by_logging_level(self, requested_level: LoggingLevel) -> list[Log]:
        fetched_logs: list[Log] = []
        for log in logs:
            if requested_level == log.logging_level:
                fetched_logs.append(log)
        return fetched_logs

    def output_logs(self) -> None:
        with open("logs.txt", "w+") as outputted_logs:
            for log in logs:
                outputted_logs.write(str(log) + "\n")
