from django.shortcuts import render, redirect, get_object_or_404

from .models import Employer, HiringOffer
from jobs.models import Job
from students.models import Application


# =========================================================
# EMPLOYER REGISTER
# =========================================================

def employer_register(request):

    if request.method == "POST":

        company_name = request.POST.get("company_name", "").strip()
        company_email = request.POST.get("company_email", "").strip()
        phone = request.POST.get("phone", "").strip()
        location = request.POST.get("location", "").strip()
        password = request.POST.get("password", "").strip()

        if not company_name or not company_email or not phone or not location or not password:
            return render(
                request,
                "employer_registration.html",
                {
                    "error": "Please fill all required fields."
                }
            )

        if Employer.objects.filter(company_email=company_email).exists():
            return render(
                request,
                "employer_registration.html",
                {
                    "error": "Company email already exists."
                }
            )

        Employer.objects.create(
            company_name=company_name,
            company_email=company_email,
            phone=phone,
            location=location,
            password=password
        )

        return redirect("employer_login")

    return render(
        request,
        "employer_registration.html"
    )


# =========================================================
# EMPLOYER LOGIN
# =========================================================

def employer_login(request):

    if request.method == "POST":

        company_email = request.POST.get(
            "company_email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()

        employer = Employer.objects.filter(
            company_email=company_email,
            password=password
        ).first()

        if employer:

            request.session["employer_id"] = employer.id

            return redirect(
                "employer_dashboard"
            )

        return render(
            request,
            "employer_login.html",
            {
                "error": "Invalid Email or Password"
            }
        )

    return render(
        request,
        "employer_login.html"
    )


# =========================================================
# EMPLOYER LOGOUT
# =========================================================

def employer_logout(request):

    request.session.flush()

    return redirect(
        "employer_login"
    )


# =========================================================
# POST JOB
# =========================================================

def post_job(request):

    employer_id = request.session.get("employer_id")

    if not employer_id:
        return redirect("employer_login")

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    if request.method == "POST":

        job = Job.objects.create(

            job_title=request.POST.get(
                "job_title"
            ),

            job_type=request.POST.get(
                "job_type"
            ),

            company_name=request.POST.get("company_name"),

            employer_email=employer.company_email,

            location=request.POST.get(
                "location"
            ),

            salary=request.POST.get(
                "salary"
            ),

            experience=request.POST.get(
                "experience"
            ),

            skills=request.POST.get(
                "skills"
            )
        )

        print("NEW JOB ID:", job.id)
        print("NEW JOB COMPANY:", job.company_name)

        return redirect(
            "employer_dashboard"
        )

    return render(
        request,
        "post_job.html",
        {
            "employer": employer
        }
    )

# =========================================================
# EMPLOYER DASHBOARD
# =========================================================
# =========================================================
# EMPLOYER DASHBOARD
# =========================================================

def employer_dashboard(request):

    employer_id = request.session.get("employer_id")

    if not employer_id:
        return redirect("employer_login")

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    # -----------------------------------------
    # EMPLOYER JOBS
    # -----------------------------------------

    jobs = Job.objects.filter(
        employer_email=employer.company_email
    ).order_by("-id")

    # -----------------------------------------
    # APPLICATIONS FOR EMPLOYER JOBS
    # -----------------------------------------

    applications = Application.objects.filter(
        job__in=jobs
    ).order_by("-id")

    # -----------------------------------------
    # JOB COUNT
    # -----------------------------------------

    total_jobs = jobs.count()

    # -----------------------------------------
    # APPLICATION COUNTS
    # -----------------------------------------

    total_applicants = applications.count()

    accepted_applications = applications.filter(
        status="Accepted"
    ).count()

    rejected_applications = applications.filter(
        status="Rejected"
    ).count()

    pending_applications = applications.filter(
        status="Applied"
    ).count()

    # -----------------------------------------
    # HIRING OFFERS
    # -----------------------------------------

   # -----------------------------------------
   # HIRING OFFERS
   # -----------------------------------------

    hiring_offers = HiringOffer.objects.filter(
    application__job__in=jobs
    ).order_by("-id")

    total_hiring_offers = hiring_offers.count()

    accepted_hiring_offers = hiring_offers.filter(
    status="Accepted"
    ).count()

    rejected_hiring_offers = hiring_offers.filter(
    status="Rejected"
    ).count()

    pending_hiring_offers = hiring_offers.filter(
    status="Offered"
    ).count()
    # =====================================================
    # DEBUG - JOBS
    # =====================================================

    print()
    print("========== EMPLOYER DASHBOARD DEBUG ==========")

    print(
        "EMPLOYER:",
        employer.company_name
    )

    print(
        "EMPLOYER EMAIL:",
        employer.company_email
    )

    print()
    print("---------- JOBS ----------")

    print(
        "JOB COUNT:",
        jobs.count()
    )

    for job in jobs:

        print(
            "JOB:",
            job.id,
            "| TITLE:",
            job.job_title,
            "| COMPANY:",
            job.company_name,
            "| EMAIL:",
            job.employer_email
        )

    # =====================================================
    # DEBUG - APPLICATIONS
    # =====================================================

    print()
    print("---------- APPLICATIONS ----------")

    print(
        "APPLICATION COUNT:",
        applications.count()
    )

    for application in applications:

        print(
            "APPLICATION:",
            application.id,
            "| STUDENT:",
            application.student_name,
            "| EMAIL:",
            application.student_email,
            "| JOB:",
            application.job_title,
            "| STATUS:",
            application.status
        )

    # =====================================================
    # DEBUG - APPLICATION COUNTS
    # =====================================================

    print()
    print("---------- APPLICATION COUNTS ----------")

    print(
        "TOTAL APPLICANTS:",
        total_applicants
    )

    print(
        "ACCEPTED APPLICATIONS:",
        accepted_applications
    )

    print(
        "REJECTED APPLICATIONS:",
        rejected_applications
    )

    print(
        "PENDING APPLICATIONS:",
        pending_applications
    )

    # =====================================================
    # DEBUG - HIRING OFFERS
    # =====================================================

    print()
    print("---------- HIRING OFFERS ----------")

    print(
        "TOTAL HIRING OFFERS:",
        total_hiring_offers
    )

    print(
        "PENDING HIRING OFFERS:",
        pending_hiring_offers
    )

    print(
        "ACCEPTED HIRING OFFERS:",
        accepted_hiring_offers
    )

    print(
        "REJECTED HIRING OFFERS:",
        rejected_hiring_offers
    )

    for offer in hiring_offers:

        print(
            "OFFER ID:",
            offer.id,
            "| STUDENT:",
            offer.student_name,
            "| COMPANY:",
            offer.company_name,
            "| JOB:",
            offer.job_title,
            "| STATUS:",
            offer.status
        )

    print()
    print("==============================================")
    print()

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "employer": employer,

        "jobs": jobs,

        "total_jobs":
            total_jobs,

        "total_applicants":
            total_applicants,

        "accepted_applications":
            accepted_applications,

        "rejected_applications":
            rejected_applications,

        "pending_applications":
            pending_applications,

        "total_hiring_offers":
            total_hiring_offers,

        "pending_hiring_offers":
            pending_hiring_offers,

        "accepted_hiring_offers":
            accepted_hiring_offers,

        "rejected_hiring_offers":
            rejected_hiring_offers,
    }

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "employer_dashboard.html",
        context
    )
# =========================================================
# MY JOBS
# =========================================================

def my_jobs(request):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    jobs = Job.objects.filter(
        employer_email__iexact=employer.company_email
    ).order_by("-id")

    return render(
        request,
        "my_jobs.html",
        {
            "jobs": jobs,
            "employer": employer
        }
    )


# =========================================================
# EDIT JOB
# =========================================================

def edit_job(request, job_id):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer_email__iexact=employer.company_email
    )

    if request.method == "POST":

        job.job_title = request.POST.get(
            "job_title",
            ""
        ).strip()

        job.job_type = request.POST.get(
            "job_type",
            ""
        ).strip()

        job.location = request.POST.get(
            "location",
            ""
        ).strip()

        job.salary = request.POST.get(
            "salary",
            ""
        ).strip()

        job.experience = request.POST.get(
            "experience",
            ""
        ).strip()

        job.skills = request.POST.get(
            "skills",
            ""
        ).strip()

        job.description = request.POST.get(
            "description",
            ""
        ).strip()

        # Keep company information connected
        job.company_name = employer.company_name
        job.employer_email = employer.company_email

        job.save()

        return redirect(
            "my_jobs"
        )

    return render(
        request,
        "edit_job.html",
        {
            "job": job,
            "employer": employer
        }
    )


# =========================================================
# DELETE JOB
# =========================================================

def delete_job(request, job_id):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer_email__iexact=employer.company_email
    )

    if request.method == "POST":

        job.delete()

        return redirect(
            "employer_dashboard"
        )

    return render(
        request,
        "delete_job.html",
        {
            "job": job,
            "employer": employer
        }
    )


# =========================================================
# VIEW APPLICANTS
# =========================================================

def view_applicants(request, job_id):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer_email__iexact=employer.company_email
    )

    applications = Application.objects.filter(
        job=job
    ).order_by("-id")

    print()
    print("========== VIEW APPLICANTS ==========")
    print("JOB ID:", job.id)
    print("JOB TITLE:", job.job_title)
    print("COMPANY:", job.company_name)
    print(
        "APPLICATION COUNT:",
        applications.count()
    )

    for application in applications:

        print(
            "APPLICATION:",
            application.id,
            "| STUDENT:",
            application.student_name,
            "| STATUS:",
            application.status
        )

    print("=====================================")
    print()

    return render(
        request,
        "employers/view_applicants.html",
        {
            "employer": employer,
            "job": job,
            "applications": applications,
        }
    )


# =========================================================
# EMPLOYER PROFILE
# =========================================================

def employer_profile(request):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    return render(
        request,
        "employer_profile.html",
        {
            "employer": employer
        }
    )


# =========================================================
# EDIT EMPLOYER PROFILE
# =========================================================

def edit_employer_profile(request):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    old_email = employer.company_email

    if request.method == "POST":

        company_name = request.POST.get(
            "company_name",
            ""
        ).strip()

        company_email = request.POST.get(
            "company_email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        # -----------------------------------------
        # EMAIL DUPLICATE CHECK
        # -----------------------------------------

        if Employer.objects.filter(
            company_email=company_email
        ).exclude(
            id=employer.id
        ).exists():

            return render(
                request,
                "employers/edit_employer_profile.html",
                {
                    "employer": employer,
                    "error":
                        "This company email already exists."
                }
            )

        employer.company_name = company_name
        employer.company_email = company_email
        employer.phone = phone
        employer.location = location

        employer.save()

        # -----------------------------------------
        # IMPORTANT
        # Update employer email in existing jobs
        # -----------------------------------------

        Job.objects.filter(
            employer_email=old_email
        ).update(
            employer_email=company_email,
            company_name=company_name
        )

        return redirect(
            "employer_dashboard"
        )

    return render(
        request,
        "employers/edit_employer_profile.html",
        {
            "employer": employer
        }
    )


# =========================================================
# ACCEPT APPLICATION
# =========================================================

def accept_application(
    request,
    application_id
):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer_email__iexact=employer.company_email
    )

    application.status = "Accepted"

    application.save()

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# =========================================================
# REJECT APPLICATION
# =========================================================

def reject_application(
    request,
    application_id
):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer_email__iexact=employer.company_email
    )

    application.status = "Rejected"

    application.save()

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# =========================================================
# SEND HIRING OFFER
# =========================================================

def send_hiring_offer(
    request,
    application_id
):

    employer_id = request.session.get(
        "employer_id"
    )

    if not employer_id:
        return redirect(
            "employer_login"
        )

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    # =====================================================
    # GET APPLICATION
    # =====================================================

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer_email__iexact=employer.company_email
    )

    # =====================================================
    # ONLY ACCEPTED APPLICATION
    # =====================================================

    if application.status != "Accepted":

        return redirect(
            "view_applicants",
            job_id=application.job.id
        )

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        salary = request.POST.get(
            "salary",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        offer_message = request.POST.get(
            "offer_message",
            ""
        ).strip()

        # -----------------------------------------
        # BASIC VALIDATION
        # -----------------------------------------

        if not salary or not location or not offer_message:

            return render(
                request,
                "employers/send_hiring_offer.html",
                {
                    "application": application,
                    "employer": employer,
                    "error":
                        "Please fill all offer details."
                }
            )

        # =================================================
        # CREATE / UPDATE OFFER
        # =================================================

        offer, created = HiringOffer.objects.update_or_create(

            application=application,

            defaults={

                "student_name":
                    application.student_name,

                "student_email":
                    application.student_email,

                "job_title":
                    application.job_title,

                "company_name":
                    employer.company_name,

                "salary":
                    salary,

                "location":
                    location,

                "offer_message":
                    offer_message,

                "status":
                    "Offered",
            }
        )

        print()
        print("========== HIRING OFFER ==========")
        print("OFFER ID:", offer.id)
        print("APPLICATION ID:", application.id)
        print(
            "STUDENT:",
            offer.student_name
        )
        print(
            "EMAIL:",
            offer.student_email
        )
        print(
            "COMPANY:",
            offer.company_name
        )
        print(
            "JOB:",
            offer.job_title
        )
        print(
            "STATUS:",
            offer.status
        )
        print(
            "CREATED:",
            created
        )
        print("==================================")
        print()

        return redirect(
            "view_applicants",
            job_id=application.job.id
        )

    # =====================================================
    # GET
    # =====================================================

    return render(
        request,
        "employers/send_hiring_offer.html",
        {
            "application": application,
            "employer": employer
        }
    )


# =========================================================
# EMPLOYER HIRING OFFERS
# =========================================================
# -----------------------------------------
# EMPLOYER HIRING OFFERS
# -----------------------------------------

def employer_hiring_offers(request):

    employer_id = request.session.get("employer_id")

    if not employer_id:
        return redirect("employer_login")

    employer = get_object_or_404(
        Employer,
        id=employer_id
    )

    # -----------------------------------------
    # THIS EMPLOYER'S HIRING OFFERS
    # -----------------------------------------

    offers = HiringOffer.objects.filter(
        company_name=employer.company_name
    ).order_by("-id")

    # -----------------------------------------
    # COUNTS
    # -----------------------------------------

    total_hiring_offers = offers.count()

    accepted_hiring_offers = offers.filter(
        status="Accepted"
    ).count()

    rejected_hiring_offers = offers.filter(
        status="Rejected"
    ).count()

    pending_hiring_offers = offers.filter(
        status="Offered"
    ).count()

    return render(
        request,
        "employers/hiring_offers.html",
        {
            "employer": employer,
            "offers": offers,
            "total_hiring_offers": total_hiring_offers,
            "accepted_hiring_offers": accepted_hiring_offers,
            "rejected_hiring_offers": rejected_hiring_offers,
            "pending_hiring_offers": pending_hiring_offers,
        }
    )