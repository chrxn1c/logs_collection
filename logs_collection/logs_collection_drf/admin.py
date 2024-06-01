from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import User, Log, LoggingLevel

admin.site.register([User, Log, LoggingLevel])
