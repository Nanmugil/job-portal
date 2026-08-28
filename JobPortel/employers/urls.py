from django.urls import path
from .views import employer_register,employer_login,post_job
from .views import view_applicants,employer_logout
from .views import my_jobs
from .views import edit_job
from .views import delete_job
from .import views


urlpatterns = [

    # ==============================
    # EMPLOYER AUTHENTICATION
    # ==============================

    path(
        "register/",
        views.employer_register,
        name="employer_register"
    ),

    path(
        "login/",
        views.employer_login,
        name="employer_login"
    ),

    path(
        "logout/",
        views.employer_logout,
        name="employer_logout"
    ),


    # ==============================
    # EMPLOYER DASHBOARD
    # ==============================

    path(
        "dashboard/",
        views.employer_dashboard,
        name="employer_dashboard"
    ),


    # ==============================
    # JOB MANAGEMENT
    # ==============================

    path(
        "post-job/",
        views.post_job,
        name="post_job"
    ),

    path(
        "my-jobs/",
        views.my_jobs,
        name="my_jobs"
    ),

    path(
        "edit-job/<int:job_id>/",
        views.edit_job,
        name="edit_job"
    ),

    path(
        "delete-job/<int:job_id>/",
        views.delete_job,
        name="delete_job"
    ),


    # ==============================
    # APPLICANTS
    # ==============================

    path(
        "view-applicants/<int:job_id>/",
        views.view_applicants,
        name="view_applicants"
    ),

    path(
        "accept-application/<int:application_id>/",
        views.accept_application,
        name="accept_application"
    ),

    path(
        "reject-application/<int:application_id>/",
        views.reject_application,
        name="reject_application"
    ),


    # ==============================
    # HIRING OFFERS
    # ==============================

    path(
        "send-hiring-offer/<int:application_id>/",
        views.send_hiring_offer,
        name="send_hiring_offer"
    ),

    path(
        "hiring-offers/",
        views.employer_hiring_offers,
        name="employer_hiring_offers"
    ),


    # ==============================
    # EMPLOYER PROFILE
    # ==============================

    path(
        "profile/",
        views.employer_profile,
        name="employer_profile"
    ),

    path(
        "edit-profile/",
        views.edit_employer_profile,
        name="edit_employer_profile"
    ),
]
