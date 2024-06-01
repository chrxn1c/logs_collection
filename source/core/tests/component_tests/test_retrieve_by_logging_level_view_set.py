from core.views import UserViewSet
from django.test import TransactionTestCase, RequestFactory

from core.views import LogViewSet, RetrieveByLoggingLevelViewSet

from core.views import RetrieveByLoggingLevelViewSet

from core.services.notification_service import NotificationService


class TestRetrieveByLoggingLevelViewSet(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.notification_service = NotificationService()
        self.notification_service.setup_standard_logging_levels()

    def test_retrieve_by_logging_level_empty(self):
        request = self.factory.post('/api/users',
                                    {'first_name': "Dmitry", 'second_name': 'Alimsky'})
        response = UserViewSet.as_view({'post': 'create'})(request)

        request = self.factory.post('/api/logs',
                                    {'user_id': response.data['id'], 'logging_level': 30,
                                     'message': 'testing_posting_a_log_failure'})

        response = LogViewSet.as_view({'post': 'create'})(request)

        request = self.factory.get('/api/logs/CRITICAL')
        response = RetrieveByLoggingLevelViewSet.as_view({'get': 'retrieve_by_logging_level'})(request, logging_level_name="CRITICAL")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_by_logging_level_not_empty(self):
        # create a user
        request = self.factory.post('/api/users',
                                    {'first_name': "Dmitry", 'second_name': 'Alimsky'})
        user_response = UserViewSet.as_view({'post': 'create'})(request)


        # create a log

        request = self.factory.post('/api/logs',
                                    {'user_id': user_response.data['id'], 'logging_level': 30,
                                     'message': 'testing_posting_a_log_success'})

        log_response = LogViewSet.as_view({'post': 'create'})(request)

        request = self.factory.get('/api/logs/WARNING')
        response = RetrieveByLoggingLevelViewSet.as_view({'get': 'retrieve_by_logging_level'})(request,
                                                                                               logging_level_name="WARNING")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], log_response.data['message'])
        self.assertEqual(response.data[0]['id'], log_response.data['id'])
        self.assertEqual(response.data[0]['user_id_id'], user_response.data['id'])
        self.assertEqual(response.data[0]['logging_level_id'], log_response.data['logging_level'])