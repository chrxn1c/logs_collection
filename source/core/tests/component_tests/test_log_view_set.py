from django.test import TransactionTestCase, RequestFactory

from core.models import User, LogsPerUser

from core.views import LogViewSet

from ...services.notification_service import NotificationService

from source.core.views import UserViewSet


class TestLogViewSet(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(first_name='John', second_name='Doe')
        self.user.save()
        self.notification_service = NotificationService()
        self.notification_service.setup_standard_logging_levels()

        # previous unit tests create LogsPerUser model with previous (but now non-existing) user, which breaks
        # integrity of foreign keys, in order to avoid it I have to manually create a user with user_id = 2
        self.random_fella = User.objects.create(first_name='IFucking', second_name='HateDjango')
        self.random_fella.save()

    def test_posting_a_log_failure(self):
        request = self.factory.post('/api/users',
                                    {'first_name': "Dmitry", 'second_name': 'Doe'})
        response = UserViewSet.as_view({'post': 'create'})(request)

        request = self.factory.post('/api/logs',
                                    {'user_id': response.data['id'],
                                     'message': 'testing_posting_a_log_failure'})
        response = LogViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, 400)

    def test_posting_a_log_success(self):
        request = self.factory.post('/api/users',
                                    {'first_name': "Dmitry", 'second_name': 'Doe'})
        response = UserViewSet.as_view({'post': 'create'})(request)

        request = self.factory.post('/api/logs',
                                    {'user_id': response.data['id'], 'logging_level': 30,
                                     'message': 'testing_posting_a_log_failure'})
        response = LogViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, 201)