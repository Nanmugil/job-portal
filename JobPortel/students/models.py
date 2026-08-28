from django.db import models


class Student(models.Model):
    full_name= models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True)
    password = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100,blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    skills = models.CharField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resume=models.FileField(upload_to="resumes/", blank=True,null=True)

    def __str__(self):
        return self.full_name

class JobApplication(models.Model):

    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student_name



class Application(models.Model):

    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    student_name = models.CharField(max_length=100)

    student_email = models.EmailField()

    job_title = models.CharField(max_length=200)

    company_name = models.CharField(max_length=200)

    location = models.CharField(max_length=200, blank=True)

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student_name} - {self.job_title}"