from django.test import TestCase

from core.models import User, LoggingLevel, Log, Notification, LogsPerUser
from core.services.notification_service import NotificationService

from core.serializers import LogSerializer, LogPerUserSerializer


class NotificationServiceTestCase(TestCase):
    service = NotificationService()

    def set_up(self):
        self.service.setup_standard_logging_levels()

    def test_getting_notifications(self):
        user = User.objects.create(first_name='John', second_name="Doe")\

        # previous unit tests create LogsPerUser model with previous (but now non-existing) user, which breaks
        # integrity of foreign keys, in order to avoid it I have to manually create a user with user_id = 2
        random_fella = User.objects.create(first_name='Jane', second_name='Doe')

        user.save()
        random_fella.save()

        LoggingLevel.objects.get_or_create(id=50, logging_level_name="CRITICAL")
        critical_level = LoggingLevel.objects.get(id=50)

        for i in range(15):
            critical_log = Log.objects.create(user_id=user, logging_level=critical_level,
                                              message="This is a error message")
            critical_log.save()
            added_log = Log.objects.get(id=i + 1)
            serialized_log = LogSerializer(added_log)
            self.service.add_log_entry(serialized_log.data)

        result = self.service.get_notifications_of_user(user.id)

        assert len(result) == 1
        serialized_result = result[0]
        assert serialized_result["id"] == 1
        assert serialized_result["user_id"] == 1
        assert serialized_result["message"] == "user 1 has 10 logs with ERROR level"

    def test_creating_default_logging_levels(self):
        existing_logging_levels = LoggingLevel.objects.all().values()

        assert len(existing_logging_levels) == 5
        assert existing_logging_levels[0]["id"] == 10 and existing_logging_levels[0]["logging_level_name"] == "DEBUG"
        assert existing_logging_levels[1]["id"] == 20 and existing_logging_levels[1]["logging_level_name"] == "INFO"
        assert existing_logging_levels[2]["id"] == 30 and existing_logging_levels[2]["logging_level_name"] == "WARNING"
        assert existing_logging_levels[3]["id"] == 40 and existing_logging_levels[3]["logging_level_name"] == "ERROR"
        assert existing_logging_levels[4]["id"] == 50 and existing_logging_levels[4]["logging_level_name"] == "CRITICAL"


    def test_not_adding_log_entry(self):
        user = User.objects.create(first_name='Max', second_name='Berezhnoy')
        user.save()

        # previous unit tests create LogsPerUser model with previous (but now non-existing) user, which breaks
        # integrity of foreign keys, in order to avoid it I have to manually create a user with user_id = 2
        random_fella = User.objects.create(first_name='Jane', second_name='Doe')
        random_fella.save()

        logging_level = LoggingLevel.objects.get(id=50)
        log = Log.objects.create(user_id=user, logging_level=logging_level, message="Max Berezhnoy Debug Message")
        log.save()

        serialized_log = LogSerializer(log).data
        self.service.add_log_entry(serialized_log)

        logs_per_user_of_current_user = LogsPerUser.objects.all().filter(user__id=user.id).values()[0]
        assert logs_per_user_of_current_user["user_id"] == user.id
        assert logs_per_user_of_current_user["counter"] == 0