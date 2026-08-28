from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "job_title",
        "job_type",
        "company_name",
        "employer_email",
        "location",
        "salary",
        "experience",
    )

    search_fields = (
        "job_title",
        "company_name",
        "employer_email",
        "location",
        "skills",
    )

    list_filter = (
        "job_type",
        "company_name",
        "location",
    )

    ordering = (
        "-id",
    )