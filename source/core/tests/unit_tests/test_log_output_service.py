from django.test import TestCase



class LogOutputServiceTestCase(TestCase):
    def set_up(self):
        self.service = LogOutputService()

    def test_print_logs_to_file(self):
        self.service.print_logs_to_file()
        path = Path(__file__).parent.parent.parent / "static/logs.txt"
        assert path.is_file()