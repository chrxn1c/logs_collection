from django.test import TransactionTestCase, RequestFactory

from core.models import User, LogsPerUser

from core.models import LoggingLevel
from core.views import LogViewSet

from core.services.notification_service import NotificationService


class TestLogViewSet(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(first_name='John', second_name='Doe')
        self.user.save()
        self.notification_service = NotificationService()
        self.notification_service.setup_standard_logging_levels()

    # def test_posting_a_log_failure(self):
    #     request = self.factory.post('/api/logs',
    #                                 {'user_id': self.user.id, 'logging_level': 40, 'message': 'testing_posting_a_log_failure'})
    #     response = LogViewSet.as_view({'post': 'create'})(request)
    #
    #     self.assertEqual(response.status_code, 401)

    def test_posting_a_log_success(self):
        request = self.factory.post('/api/logs',
                                    {'user_id': self.user.id, 'logging_level': 40, 'message': 'testing_posting_a_log_success'})
        response = LogViewSet.as_view({'post': 'create'})(request)
        print(response.data)
        self.assertEqual(response.status_code, 201)

