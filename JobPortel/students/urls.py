from django.urls import path
from.views import student_register,student_login,student_dashboard,job_details,apply_job
from .views import student_profile
from .views import edit_student_profile
from .views import student_logout
from .views import my_applications
from .import views

urlpatterns = [
    path("register/", student_register, name="student_register"),
    path("login/", student_login, name="student_login"),
    path("dashboard/", student_dashboard, name="student_dashboard"),

    path("profile/", views.student_profile, name="student_profile"),
    path("edit-profile/", views.edit_student_profile, name="edit_student_profile"),

    path("logout/", views.student_logout, name="student_logout"),
    path("my-applications/", my_applications, name="my_applications"),

    path("job-details/<int:id>/", views.job_details, name="job_details"),
    path("apply-job/<int:job_id>/", views.apply_job, name="apply_job"),

    path("my-hiring-offers/",views.my_hiring_offers,name="my_hiring_offers"),
    path("update-hiring-offer/<int:offer_id>/<str:status>/", views.update_hiring_offer_status, name="update_hiring_offer_status"),
    path("accept-hiring-offer/<int:offer_id>/", views.accept_hiring_offer, name="accept_hiring_offer"),

    path("reject-hiring-offer/<int:offer_id>/", views.reject_hiring_offer, name="reject_hiring_offer"),
]
