from uuid import UUID

from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from core import serializers
from core import models
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from core.models import Notification, User
from core.serializers import LogSerializer, NotificationSerializer, OperationSerializer, \
    GetOperationQuerySerializer, ApiErrorSerializer
from core.services.log_output_service import LogOutputService
from core.services.notification_service import NotificationService
from core.services.operation_service import OperationService
from core.services.retrieve_by_logging_level_service import RetrieveByLoggingLevelService


class UserViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


@extend_schema_view(
    create=extend_schema(
        summary="Post new log",
        request=LogSerializer,
        responses={
            status.HTTP_201_CREATED: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: None,
        },
        auth=None
    )
)
class LogViewSet(ModelViewSet):
    notification_service = NotificationService()
    log_output_service = LogOutputService()

    lookup_field = 'id'
    serializer_class = serializers.LogSerializer
    queryset = models.Log.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = serializers.LogSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.notification_service.add_log_entry(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoggingLevelViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = serializers.LoggingLevelSerializer
    queryset = models.LoggingLevel.objects.all()


@extend_schema_view(
    get_notifications_of_user=extend_schema(
        summary="Get notifications of chosen user",
        request=NotificationSerializer,
        responses={
            status.HTTP_404_NOT_FOUND: serializers.ApiErrorSerializer,
            status.HTTP_200_OK: NotificationSerializer
        }
    )
)
class NotificationViewSet(ModelViewSet):
    lookup_field = 'id'
    serializer_class = serializers.NotificationSerializer
    queryset = models.Notification.objects.all()

    def get_notifications_of_user(self, request, user_id):
        data = ""
        try:
            data = NotificationService.get_notifications_of_user(user_id=user_id)
        except User.DoesNotExist:
            return Response(data={"error": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=data, status=status.HTTP_200_OK)


@extend_schema_view(
    retrieve_by_logging_level=extend_schema(
        summary='Get all logs by preferred logging level',
        request=LoggingLevelViewSet,
        responses={
            status.HTTP_200_OK: serializers.LogSerializer(many=True),
            status.HTTP_404_NOT_FOUND: serializers.ApiErrorSerializer
        },
        auth=None,
    )
)
class RetrieveByLoggingLevelViewSet(ModelViewSet):
    @action(detail=False, methods=["GET"])
    def retrieve_by_logging_level(self, request, logging_level_name):
        query_serializer = serializers.RetrieveByLoggingLevelSerializer(data={"logging_level_name": logging_level_name})

        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = RetrieveByLoggingLevelService.get_logs_by_logging_level(logging_level_name)
        return Response(data=data, status=status.HTTP_200_OK)


@extend_schema_view(
    request=extend_schema(
        summary="Request operation of getting all logs to a text file",
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_400_BAD_REQUEST: ApiErrorSerializer,
        },
        auth=None,
    ),
    status=extend_schema(
        summary="Get status of operation of getting all logs to a text file",
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_404_NOT_FOUND: ApiErrorSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ApiErrorSerializer,
        }
    )
)

class LogFileOutputViewSet(ViewSet):
    operation_service = OperationService()
    log_output_service = LogOutputService()

    @action(detail=False, methods=["GET"])
    def request(self, request, *args, **kwargs):
        if request.data:
            return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)

        operation_id = self.operation_service.execute_operation(self.log_output_service.print_logs_to_file)
        operation = self.operation_service.get_operation(operation_id)

        return Response(
            data=OperationSerializer(operation).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["GET"])
    def status(self, request, *args, **kwargs):
        query = GetOperationQuerySerializer(data=request.query_params)
        if not query.is_valid():
            return Response(data=query.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        print(query.validated_data)

        operation = self.operation_service.get_operation(UUID(query.data.get("id")))
        if operation is None:
            return Response(data=query.errors, status=status.HTTP_404_NOT_FOUND)

        response = self.log_output_service.print_logs_to_file()
        print(operation)
        return Response(status=status.HTTP_200_OK,
                        data=OperationSerializer(
                            {
                                "id": operation.id,
                                "done": operation.done,
                                "result": {
                                    "path": operation.result,
                                },
                            }
                        ).data,
                        )
