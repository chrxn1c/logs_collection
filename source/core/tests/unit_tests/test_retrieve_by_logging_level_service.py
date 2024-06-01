import logging

from django.test import TestCase

from core.models import User, Log, LoggingLevel
from core.services.retrieve_by_logging_level_service import RetrieveByLoggingLevelService


class TestOperationService(TestCase):
    def setUp(self):
        self.service = RetrieveByLoggingLevelService()

    def test_retrieve_by_logging_level(self):
        user = User.objects.create(first_name='John', second_name="Doe")
        user.save()

        warning_level = LoggingLevel.objects.get(id=30)
        error_level = LoggingLevel.objects.get(id=40)
        critical_level = LoggingLevel.objects.get(id=50)

        warning_log = Log.objects.create(user_id=user, logging_level=warning_level, message="This is a warning message")
        error_log = Log.objects.create(user_id=user, logging_level=error_level, message="This is a error message")
        critical_log = Log.objects.create(user_id=user, logging_level=critical_level, message="This is a critical message")

        warning_log.save()
        error_log.save()
        critical_log.save()

        result = self.service.get_logs_by_logging_level("CRITICAL")

        assert len(result) == 1

        result = result[0]

        assert result["id"] == 3
        assert result["user_id_id"] == 1
        assert result["logging_level_id"] == 50
        assert result["message"] == "This is a critical message"

