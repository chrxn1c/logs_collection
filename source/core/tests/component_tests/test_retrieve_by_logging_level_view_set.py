from core.views import UserViewSet
from django.test import TransactionTestCase, RequestFactory

from core.views import LogViewSet, RetrieveByLoggingLevelViewSet

from core.views import RetrieveByLoggingLevelViewSet


class TestRetrieveByLoggingLevelViewSet(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()

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
