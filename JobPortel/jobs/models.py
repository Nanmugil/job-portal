from django.db import models


class Job(models.Model):

    job_title = models.CharField(
        max_length=100
    )

    job_type = models.CharField(
        max_length=20,
        choices=[
            ("Job", "Job"),
            ("Internship", "Internship"),
        ],
        default="Job"
    )

    company_name = models.CharField(
        max_length=100,
        default="Unknown Company"
    )

    employer_email = models.EmailField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    salary = models.CharField(
        max_length=50,
        default="Not specified"
    )

    experience = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    skills = models.TextField(
        default=""
    )

    def __str__(self):
        return self.job_title


class Application(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    student_name = models.CharField(
        max_length=100
    )

    student_email = models.EmailField()

    job_title = models.CharField(
        max_length=100
    )

    company_name = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=30,
        default="Applied"
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.student_name

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
        max_length=100
    )

    company_name = models.CharField(
        max_length=100
    )

    salary = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    offer_message = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default="Offered"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            self.student_name
            + " - "
            + self.job_title
        )