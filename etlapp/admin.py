from django.contrib import admin
from .models import StudentRaw, StudentClean, ETLLog


@admin.register(StudentRaw)
class StudentRawAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "course", "extracted_at")
    list_filter = ("course",)
    search_fields = ("name", "student_id")


@admin.register(StudentClean)
class StudentCleanAdmin(admin.ModelAdmin):
    list_display = ("student_id", "full_name", "course", "loaded_at")
    list_filter = ("course",)
    search_fields = ("full_name", "student_id")


@admin.register(ETLLog)
class ETLLogAdmin(admin.ModelAdmin):
    list_display = ("filename", "run_at", "rows_extracted", "rows_loaded", "status")
    list_filter = ("status",)
    readonly_fields = ("run_at", "rows_extracted", "rows_loaded", "status", "message")
