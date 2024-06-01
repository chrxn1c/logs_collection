from django.test import TestCase

from core.models import User, LoggingLevel, Log, Notification, LogsPerUser
from core.services.notification_service import NotificationService

from core.serializers import LogSerializer


class NotificationServiceTestCase(TestCase):
    service = NotificationService()

    def set_up(self):
        pass

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
        print(serialized_result)
        print(LogsPerUser.objects.all().values())
        assert serialized_result["id"] == 1
        assert serialized_result["user_id"] == 1
        assert serialized_result["message"] == "user 1 has 10 logs with ERROR level"
