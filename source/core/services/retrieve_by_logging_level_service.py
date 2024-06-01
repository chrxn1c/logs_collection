from rest_framework import status
from rest_framework.response import Response

from core import models


class RetrieveByLoggingLevelService:
    def __init__(self):
        pass

    @staticmethod
    def get_logs_by_logging_level(logging_level_name):
        return models.Log.objects.all().filter(logging_level__logging_level_name=logging_level_name).values()
