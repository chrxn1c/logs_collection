import logging

from ..models import Log, LogsPerUser, LoggingLevel, Notification, User


class NotificationService:
    @staticmethod
    def setup_standard_logging_levels():
        standard_logging_levels: list[LoggingLevel] = [
            LoggingLevel(
                id=logging.DEBUG,
                logging_level_name="DEBUG",
            ),
            LoggingLevel(
                id=logging.INFO,
                logging_level_name="INFO",
            ),
            LoggingLevel(
                id=logging.WARNING,
                logging_level_name="WARNING",
            ),
            LoggingLevel(
                id=logging.ERROR,
                logging_level_name="ERROR",
            ),
            LoggingLevel(
                id=logging.CRITICAL,
                logging_level_name="CRITICAL",
            ),
        ]
        for standard_logging_level in standard_logging_levels:
            standard_logging_level.save()

    @staticmethod
    def add_log_entry(log):
        logging_level = LoggingLevel.objects.get(id=log["logging_level"])
        if logging_level.id >= logging.ERROR:
            log_per_user, _ = LogsPerUser.objects.get_or_create(user__id=log["user_id"])
            log_per_user.counter += 1
            print(LogsPerUser.objects.all().values())
            log_per_user.save()

            reported_notifications_count = Notification.objects.filter(user__id=log["user_id"]).count()
            if reported_notifications_count < log_per_user.counter // 10:
                assigned_user = User.objects.get(id=log["user_id"])
                Notification.objects.create(
                    user=assigned_user,
                    message=f"user {log["user_id"]} has {log_per_user.counter} logs with ERROR level",
                )

    @staticmethod
    def get_notifications_of_user(user_id):
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise User.DoesNotExist

        return Notification.objects.filter(user__id=user_id).order_by("-id").values()
