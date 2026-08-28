from django.contrib import admin
from .models import Employer, HiringOffer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "company_name",
        "company_email",
        "phone",
        "location",
    )

    search_fields = (
        "company_name",
        "company_email",
        "phone",
        "location",
    )

    list_filter = (
        "location",
    )

    ordering = (
        "id",
    )


@admin.register(HiringOffer)
class HiringOfferAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student_name",
        "student_email",
        "company_name",
        "job_title",
        "salary",
        "location",
        "status",
        "created_at",
    )

    search_fields = (
        "student_name",
        "student_email",
        "company_name",
        "job_title",
    )

    list_filter = (
        "status",
        "company_name",
    )

    ordering = (
        "-created_at",
    )