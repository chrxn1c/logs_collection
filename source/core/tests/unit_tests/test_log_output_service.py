from django.test import TestCase
from pathlib import Path
import os

from source.core import services


class LogOutputServiceTestCase(TestCase):
    def set_up(self):
        self.service = services.LogOutputService()
        self.service.print_logs_to_file()

    def test_print_logs_to_file(self):
        path = Path(__file__).parent.parent.parent.parent.parent / "static/logs.txt"
        assert os.path.exists(str(path))