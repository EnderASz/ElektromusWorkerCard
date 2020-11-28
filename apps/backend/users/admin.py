from django.contrib import admin
from .models import (
    Worker,
    WorkTimestamp,
    AdditionalWorkTime)


# Register your models here.

admin.site.register(Worker)
admin.site.register(WorkTimestamp)
admin.site.register(AdditionalWorkTime)