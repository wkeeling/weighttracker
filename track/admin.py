from django.contrib import admin

from .models import WeightMeasurement, WeightRecord


class WeightRecordAdmin(admin.ModelAdmin):
    ordering = ['person__username']


class WeightMeasurementAdmin(admin.ModelAdmin):
    ordering = ['-created']


admin.site.register(WeightRecord, WeightRecordAdmin)
admin.site.register(WeightMeasurement, WeightMeasurementAdmin)
