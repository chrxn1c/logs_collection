from django.test import TestCase
from pathlib import Path



class LogOutputServiceTestCase(TestCase):
    def set_up(self):
        self.service = LogOutputService()
        self.service.print_logs_to_file()

    def test_print_logs_to_file(self):
        path = Path(__file__).parent.parent.parent / "static/logs.txt"
        print(path)
        print(path.is_file())
        assert path.is_file()