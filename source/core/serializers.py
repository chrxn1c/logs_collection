from rest_framework import serializers
from core import models


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class LoggingLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LoggingLevel
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = '__all__'


class RetrieveByLoggingLevelSerializer(serializers.Serializer):
    # class Meta:
    #     model = models.LoggingLevel
    #     fields = ('logging_level_name',)

    logging_level_name = serializers.CharField(max_length=10, required=True)

    def validate_logging_level_name(self, logging_level_name: str):
        acceptable_values = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if logging_level_name not in acceptable_values:
            raise serializers.ValidationError("Such logging level is not yet supported.")

        return logging_level_name


class ApiErrorSerializer(serializers.Serializer):
    message = serializers.CharField()


class OperationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, min_length=36, max_length=36)
    done = serializers.BooleanField()
    result = serializers.DictField()


class GetOperationQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
