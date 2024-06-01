from pathlib import Path

from .. import models


class LogOutputService:
    def print_logs_to_file(self):
        logs = models.Log.objects.all().values()
        path = Path(__file__).parent.parent.parent.parent / "static/logs.txt"
        with open(path, 'w+') as log_file:
            for log in logs:
                log_file.write(str(log) + "\n")

        return str(path)
