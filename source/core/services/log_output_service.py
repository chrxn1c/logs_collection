from django.conf import settings

from .. import models
from ..models import Log, LoggingLevel
from pathlib import Path


class LogOutputService:
    # def __init__(self, log_file_name: str = "logs.txt", output_log_path: str = settings.STATIC_URL + "log/"):
    #     self.log_file_name = log_file_name
    #     self.output_log_path = output_log_path[1:] + (
    #         "/" if output_log_path[-1] != "/" else ""  # cut out first '/' to get relative path and set last '/'
    #     )
    #     self.log_file_path = self.output_log_path + self.log_file_name

        # with open(self.log_file, "w") as log_file:
        #     log_file.write(";".join(Log.__dict__.keys()) + "\n")

    # def write_entry(self, log_entry) -> None:
    #     logging_level_name = LoggingLevel.objects.get(id=log_entry["logging_level"]).logging_level_name
    #     with open(self.log_file, "a") as log_file:
    #         log_file.write(";".join(
    #             [str(log_entry["id"]),
    #              str(log_entry["date"]),
    #              str(log_entry["time"]),
    #              str(log_entry["user_id"]),
    #              logging_level_name,
    #              str(log_entry["message"])]) + "\n")

    # def get_log_file_path(self) -> str:
    #     return self.log_file_path

    def print_logs_to_file(self):
        logs = models.Log.objects.all().values()
        path = Path(__file__).parent.parent / "static/logs.txt"
        with open(path, 'w') as log_file:
            for log in logs:
                log_file.write(str(log) + "\n")

        return str(path)
