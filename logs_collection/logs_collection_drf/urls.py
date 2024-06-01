from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .services.notification_service import NotificationService
from .views import (
    LogViewSet,
    UserViewSet,
    RetrieveByLoggingLevelViewSet,
    NotificationViewSet,
    LoggingLevelViewSet,
    LogFileOutputViewSet
)
from rest_framework import routers

app_name = "logs_collection_drf"

urlpatterns = []

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'logs', LogViewSet)
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'logging_levels', LoggingLevelViewSet)

url_additional = [
    path('logs/<str:logging_level_name>', RetrieveByLoggingLevelViewSet.as_view(
        {'get': 'retrieve_by_logging_level'}
    )),
    path('notifications/<int:user_id>', NotificationViewSet.as_view(
        {'get': 'get_notifications_of_user'}
    )),
    path('logs_file/request', LogFileOutputViewSet.as_view({'get': 'request'})),
    path('logs_file/status', LogFileOutputViewSet.as_view({'get': 'status'})),

]

urlpatterns += url_additional
urlpatterns += router.urls
urlpatterns += [
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="logs_collection_drf:schema"),
        name="docs",
    ),
]

try:
    NotificationService.setup_standard_logging_levels()
except Exception as e:
    pass
