from django.db import models
from students.models import Application


# =========================================================
# EMPLOYER
# =========================================================

class Employer(models.Model):

    company_name = models.CharField(
        max_length=100
    )

    company_email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    location = models.CharField(
        max_length=100
    )

    password = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.company_name


# =========================================================
# HIRING OFFER
# =========================================================

class HiringOffer(models.Model):

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="hiring_offer"
    )

    student_name = models.CharField(
        max_length=100
    )

    student_email = models.EmailField()

    job_title = models.CharField(
        max_length=200
    )

    company_name = models.CharField(
        max_length=200
    )

    salary = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=200
    )

    offer_message = models.TextField()

    # Offered = Employer sent offer
    # Accepted = Student accepted
    # Rejected = Student rejected

    status = models.CharField(
        max_length=20,
        default="Offered"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.student_name} - "
            f"{self.job_title}"
        )