from django.test import RequestFactory, TransactionTestCase

from core.views import UserViewSet


class TestUserViewSet(TransactionTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_posting_a_log_success(self):
        request = self.factory.post('/api/users',
                                    {'first_name': "Dmitry", 'second_name': 'Doe'})
        response = UserViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, 201)

    def test_posting_a_log_failure(self):
        request = self.factory.post('/api/users',
                                    {'first_name': "ARCHIMATEBRAINDEADDEVELOPER", 'second_name': 'Doe'})
        response = UserViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, 400)
