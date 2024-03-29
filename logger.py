from log import Log, LoggingLevel
from user import User


class Logger:
    def __init__(self, trackable_users: list[User]) -> None:
        self.tracked_users: list[User] = trackable_users.copy()
        self.tracked_users_to_events_count: dict[str:int] = {}
        self._initialize_new_tracked_users_to_dict(self.tracked_users)
        self._logs: list[Log] = []

    def track_new_users(self, new_tracked_users: list[User]) -> None:
        for new_tracked_user in new_tracked_users:
            self.tracked_users.append(new_tracked_user)

        self._initialize_new_tracked_users_to_dict(new_tracked_users)

    def accept_event(self, log: Log) -> None:
        self._logs.append(log)

        if log.user not in self.tracked_users:
            return

        self.tracked_users_to_events_count[log.user] += 1
        if (self.tracked_users_to_events_count[log.user]) % 10 == 0:
            self.notify_user(log.user)

    def retrieve_by_logging_level(self, requested_level: LoggingLevel) -> list[Log]:
        fetched_logs: list[Log] = []
        for log in self._logs:
            if requested_level == log.logging_level:
                fetched_logs.append(log)
        return fetched_logs

    def notify_user(self, user: User) -> None:
        print(f"User {user.get_full_name()} now has {
              self.tracked_users_to_events_count[user]} errors!")

    def output_logs(self) -> None:
        with open("logs.txt", "w+") as outputted_logs:
            for log in self._logs:
                outputted_logs.write(str(log) + "\n")

    def _initialize_new_tracked_users_to_dict(self, new_tracked_users: list[User]) -> None:
        for new_tracked_user in new_tracked_users:
            self.tracked_users_to_events_count[new_tracked_user] = 0
