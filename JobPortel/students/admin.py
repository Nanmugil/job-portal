from django.contrib import admin
from .models import Student, Application


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "email",
        "phone",
        "course",
        "qualification",
        "location",
    )

    search_fields = (
        "full_name",
        "email",
        "course",
        "qualification",
        "location",
    )

    list_filter = (
        "course",
        "qualification",
        "location",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student_name",
        "student_email",
        "job_title",
        "company_name",
        "status",
        "applied_at",
    )

    search_fields = (
        "student_name",
        "student_email",
        "job_title",
        "company_name",
    )

    list_filter = (
        "status",
        "company_name",
    )

    ordering = (
        "-applied_at",
    )