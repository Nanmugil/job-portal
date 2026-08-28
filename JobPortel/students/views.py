from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from jobs.models import Job
from employers.models import Employer, HiringOffer

from .models import Student, JobApplication, Application


# =========================================================
# STUDENT REGISTER
# =========================================================

def student_register(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        qualification = request.POST.get("qualification", "").strip()
        course = request.POST.get("course", "").strip()
        skills = request.POST.get("skills", "").strip()
        password = request.POST.get("password", "")

        # Required field validation
        if not full_name or not email or not phone or not qualification or not password:

            return render(
                request,
                "student_registration.html",
                {
                    "error": "Please fill all required fields."
                }
            )

        # Check duplicate email
        if Student.objects.filter(email=email).exists():

            return render(
                request,
                "student_registration.html",
                {
                    "error": "Email already registered."
                }
            )

        # Create student
        Student.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            qualification=qualification,
            course=course,
            skills=skills,
            password=password
        )

        return redirect("student_login")

    return render(
        request,
        "student_registration.html"
    )


# =========================================================
# STUDENT LOGIN
# =========================================================

def student_login(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        student = Student.objects.filter(
            email=email,
            password=password
        ).first()

        if student:

            request.session["student_id"] = student.id

            return redirect("student_dashboard")

        return render(
            request,
            "student_login.html",
            {
                "error": "Invalid Email or Password"
            }
        )

    return render(
        request,
        "student_login.html"
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================
def student_dashboard(request):

    # =====================================================
    # CHECK LOGIN
    # =====================================================

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")


    # =====================================================
    # GET STUDENT
    # =====================================================

    student = get_object_or_404(
        Student,
        id=student_id
    )


    # =====================================================
    # SEARCH VALUES
    # =====================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    location = request.GET.get(
        "location",
        ""
    ).strip()

    skills = request.GET.get(
        "skills",
        ""
    ).strip()


    # =====================================================
    # ALL JOBS
    # =====================================================

    jobs = Job.objects.filter(
        job_type__iexact="Job"
    ).order_by("-id")


    # =====================================================
    # ALL INTERNSHIPS
    # =====================================================

    internships = Job.objects.filter(
        job_type__iexact="Internship"
    ).order_by("-id")


    # =====================================================
    # TOTAL COUNTS
    # =====================================================

    total_jobs = Job.objects.filter(
        job_type__iexact="Job"
    ).count()


    total_internships = Job.objects.filter(
        job_type__iexact="Internship"
    ).count()


    # =====================================================
    # SEARCH FILTER
    # =====================================================

    if search:

        jobs = jobs.filter(
        job_title__icontains=search
        )

        internships = internships.filter(
           job_title__icontains=search
        )

    # =====================================================
    # LOCATION FILTER
    # =====================================================

    if location:

        jobs = jobs.filter(
            location__icontains=location
        )

        internships = internships.filter(
            location__icontains=location
        )


    # =====================================================
    # SKILLS FILTER
    # =====================================================

    if skills:

        jobs = jobs.filter(
            skills__icontains=skills
        )

        internships = internships.filter(
            skills__icontains=skills
        )


    # =====================================================
    # STUDENT APPLICATIONS
    # =====================================================

    student_email = student.email.strip()

    applications = Application.objects.filter(
        student_email__iexact=student_email
    )

    total_applications = applications.count()


    # =====================================================
    # HIRING OFFERS
    # =====================================================

    hiring_offers = HiringOffer.objects.filter(
        student_email__iexact=student_email
    ).order_by("-id")


    # =====================================================
    # HIRING OFFER COUNTS
    # =====================================================

    hiring_offer_count = hiring_offers.count()

    offered_offers = hiring_offers.filter(
        status__in=[
            "Pending",
            "Offered"
        ]
    ).count()

    accepted_offers = hiring_offers.filter(
        status="Accepted"
    ).count()

    rejected_offers = hiring_offers.filter(
        status="Rejected"
    ).count()


    # =====================================================
    # APPLIED JOB IDS
    # =====================================================

    applied_job_ids = set(
        applications.values_list(
            "job_id",
            flat=True
        )
    )


    # =====================================================
    # DEBUG
    # =====================================================

    print()
    print("========== STUDENT DASHBOARD DEBUG ==========")

    print(
        "STUDENT:",
        student.full_name
    )

    print(
        "EMAIL:",
        repr(student.email)
    )

    print("----------------------------------------------")

    print(
        "TOTAL JOBS:",
        total_jobs
    )

    print(
        "TOTAL INTERNSHIPS:",
        total_internships
    )

    print(
        "TOTAL APPLICATIONS:",
        total_applications
    )

    print(
        "TOTAL HIRING OFFERS:",
        hiring_offer_count
    )

    print(
        "PENDING/OFFERED:",
        offered_offers
    )

    print(
        "ACCEPTED OFFERS:",
        accepted_offers
    )

    print(
        "REJECTED OFFERS:",
        rejected_offers
    )

    print("----------------------------------------------")

    # =====================================================
    # DEBUG JOBS
    # =====================================================

    print("---------- JOBS ----------")

    for job in Job.objects.all().order_by("-id"):

        print(
            "JOB ID:",
            job.id,
            "| TITLE:",
            repr(job.job_title),
            "| TYPE:",
            repr(job.job_type),
            "| COMPANY:",
            repr(job.company_name)
        )

    print("----------------------------------------------")


    # =====================================================
    # DEBUG OFFERS
    # =====================================================

    for offer in hiring_offers:

        print(
            "OFFER ID:",
            offer.id,
            "| COMPANY:",
            repr(offer.company_name),
            "| STUDENT:",
            repr(offer.student_email),
            "| JOB:",
            repr(offer.job_title),
            "| STATUS:",
            repr(offer.status)
        )

    print("==============================================")
    print()


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "student": student,

        "jobs": jobs,

        "internships": internships,

        "total_jobs": total_jobs,

        "total_internships": total_internships,

        "total_applications": total_applications,

        "hiring_offer_count": hiring_offer_count,

        "offered_offers": offered_offers,

        "accepted_offers": accepted_offers,

        "rejected_offers": rejected_offers,

        "applied_job_ids": applied_job_ids,

        "search": search,

        "location": location,

        "skills": skills,
    }


    return render(
        request,
        "student_dashboard.html",
        context
    )

# =========================================================
# STUDENT PROFILE
# =========================================================

def student_profile(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")

    student = get_object_or_404(
        Student,
        id=student_id
    )

    print()
    print("========== STUDENT PROFILE DEBUG ==========")
    print("STUDENT ID:", student.id)
    print("NAME:", student.full_name)
    print("EMAIL:", student.email)
    print("PHONE:", student.phone)
    print("COURSE:", repr(student.course))
    print("QUALIFICATION:", repr(student.qualification))
    print("LOCATION:", repr(student.location))
    print("SKILLS:", repr(student.skills))
    print("===========================================")
    print()

    return render(
        request,
        "student_profile.html",
        {
            "student": student
        }
    )


# =========================================================
# EDIT STUDENT PROFILE
# =========================================================
def edit_student_profile(request):

    # =====================================================
    # CHECK STUDENT LOGIN
    # =====================================================

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")


    # =====================================================
    # GET STUDENT
    # =====================================================

    student = get_object_or_404(
        Student,
        id=student_id
    )


    # =====================================================
    # POST - UPDATE PROFILE
    # =====================================================

    if request.method == "POST":

        print()
        print("========== EDIT STUDENT PROFILE ==========")
        print("POST DATA:", request.POST)
        print("FILES:", request.FILES)


        # =================================================
        # BASIC DETAILS
        # =================================================

        student.full_name = request.POST.get(
            "full_name",
            ""
        ).strip()


        student.email = request.POST.get(
            "email",
            ""
        ).strip()


        student.phone = request.POST.get(
            "phone",
            ""
        ).strip()


        # =================================================
        # EDUCATION DETAILS
        # =================================================

        student.course = request.POST.get(
            "course",
            ""
        ).strip()


        student.qualification = request.POST.get(
            "qualification",
            ""
        ).strip()


        # =================================================
        # OTHER DETAILS
        # =================================================

        student.location = request.POST.get(
            "location",
            ""
        ).strip()


        student.skills = request.POST.get(
            "skills",
            ""
        ).strip()


        # =================================================
        # RESUME
        # =================================================

        if request.FILES.get("resume"):

            student.resume = request.FILES.get(
                "resume"
            )


        # =================================================
        # SAVE STUDENT
        # =================================================

        student.save()


        # =================================================
        # DEBUG
        # =================================================

        print("UPDATED NAME:", student.full_name)
        print("UPDATED EMAIL:", student.email)
        print("UPDATED PHONE:", student.phone)
        print("UPDATED COURSE:", student.course)
        print(
            "UPDATED QUALIFICATION:",
            student.qualification
        )
        print("UPDATED LOCATION:", student.location)
        print("UPDATED SKILLS:", student.skills)

        print(
            "UPDATED RESUME:",
            student.resume
        )

        print("==========================================")
        print()


        # =================================================
        # REDIRECT
        # =================================================

        return redirect(
            "student_profile"
        )


    # =====================================================
    # GET - SHOW EDIT PROFILE PAGE
    # =====================================================

    return render(
        request,
        "students/edit_student_profile.html",
        {
            "student": student
        }
    )


# =========================================================
# STUDENT LOGOUT
# =========================================================

def student_logout(request):

    request.session.flush()

    return redirect(
        "student_login"
    )


# =========================================================
# MY APPLICATIONS
# =========================================================

def my_applications(request):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:
        return redirect(
            "student_login"
        )

    student = get_object_or_404(
        Student,
        id=student_id
    )

    applications = Application.objects.filter(
        student_email__iexact=student.email.strip()
    ).order_by("-id")


    return render(
        request,
        "students/my_applications.html",
        {
            "student": student,
            "applications": applications
        }
    )


# =========================================================
# JOB DETAILS
# =========================================================

def job_details(request, id):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:
        return redirect(
            "student_login"
        )

    student = get_object_or_404(
        Student,
        id=student_id
    )

    job = get_object_or_404(
        Job,
        id=id
    )


    # -----------------------------------------------------
    # CHECK ALREADY APPLIED
    # -----------------------------------------------------

    already_applied = Application.objects.filter(
        job=job,
        student_email__iexact=student.email.strip()
    ).exists()


    return render(
        request,
        "job_details.html",
        {
            "job": job,
            "student": student,
            "already_applied": already_applied
        }
    )


# =========================================================
# APPLY JOB
# =========================================================

def apply_job(request, job_id):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")

    student = get_object_or_404(
        Student,
        id=student_id
    )

    job = get_object_or_404(
        Job,
        id=job_id
    )

    # -----------------------------------------------------
    # DEBUG - JOB
    # -----------------------------------------------------

    print()
    print("========== APPLY JOB DEBUG ==========")

    print(
        "JOB ID:",
        job.id
    )

    print(
        "JOB TITLE:",
        job.job_title
    )

    print(
        "JOB COMPANY:",
        job.company_name
    )

    print(
        "JOB EMPLOYER EMAIL:",
        job.employer_email
    )

    print(
        "STUDENT:",
        student.full_name
    )

    print(
        "STUDENT EMAIL:",
        student.email
    )

    # -----------------------------------------------------
    # ONLY POST REQUEST
    # -----------------------------------------------------

    if request.method != "POST":

        return redirect(
            "job_details",
            id=job.id
        )

    # -----------------------------------------------------
    # CHECK DUPLICATE
    # -----------------------------------------------------

    already_applied = Application.objects.filter(
        job=job,
        student_email__iexact=student.email.strip()
    ).exists()

    print(
        "ALREADY APPLIED:",
        already_applied
    )

    if already_applied:

        messages.warning(
            request,
            "You have already applied for this job."
        )

        return redirect(
            "student_dashboard"
        )

    # -----------------------------------------------------
    # CREATE APPLICATION
    # -----------------------------------------------------

    application = Application.objects.create(

        job=job,

        student_name=student.full_name,

        student_email=student.email,

        job_title=job.job_title,

        company_name=job.company_name,

        resume=student.resume,

        status="Applied"
    )

    # -----------------------------------------------------
    # DEBUG - CREATED APPLICATION
    # -----------------------------------------------------

    print(
        "APPLICATION CREATED:"
    )

    print(
        "APPLICATION ID:",
        application.id
    )

    print(
        "APPLICATION JOB ID:",
        application.job.id
    )

    print(
        "APPLICATION JOB TITLE:",
        application.job.job_title
    )

    print(
        "APPLICATION COMPANY:",
        application.company_name
    )

    print(
        "APPLICATION STATUS:",
        application.status
    )

    print(
        "===================================="
    )
    print()

    messages.success(
        request,
        "Job application submitted successfully."
    )

    return redirect(
        "student_dashboard"
    )


# =========================================================
# MY HIRING OFFERS
# =========================================================

def my_hiring_offers(request):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:
        return redirect(
            "student_login"
        )

    student = get_object_or_404(
        Student,
        id=student_id
    )


    offers = HiringOffer.objects.filter(
        student_email__iexact=student.email.strip()
    ).order_by("-id")


    return render(
        request,
        "students/my_hiring_offers.html",
        {
            "student": student,
            "offers": offers
        }
    )


# =========================================================
# UPDATE HIRING OFFER STATUS
# =========================================================

def update_hiring_offer_status(
    request,
    offer_id,
    status
):

    student_id = request.session.get(
        "student_id"
    )

    if not student_id:
        return redirect(
            "student_login"
        )


    student = get_object_or_404(
        Student,
        id=student_id
    )


    offer = get_object_or_404(
        HiringOffer,
        id=offer_id,
        student_email__iexact=student.email.strip()
    )


    # -----------------------------------------------------
    # ONLY POST REQUEST
    # -----------------------------------------------------

    if request.method == "POST":

        if status == "Accepted":

            offer.status = "Accepted"

        elif status == "Rejected":

            offer.status = "Rejected"

        else:

            messages.error(
                request,
                "Invalid offer status."
            )

            return redirect(
                "my_hiring_offers"
            )


        offer.save()


        messages.success(
            request,
            f"Hiring offer {status.lower()} successfully."
        )


    return redirect(
        "my_hiring_offers"
    )


# =========================================================
# ACCEPT HIRING OFFER
# =========================================================

def accept_hiring_offer(
    request,
    offer_id
):

    if request.method != "POST":

        return redirect(
            "my_hiring_offers"
        )


    student_id = request.session.get(
        "student_id"
    )

    if not student_id:
        return redirect(
            "student_login"
        )


    student = get_object_or_404(
        Student,
        id=student_id
    )


    offer = get_object_or_404(
        HiringOffer,
        id=offer_id,
        student_email__iexact=student.email.strip()
    )


    # Only Offered/Pending offer can be accepted
    if offer.status not in [
        "Pending",
        "Offered"
    ]:

        messages.warning(
            request,
            "This hiring offer cannot be accepted."
        )

        return redirect(
            "my_hiring_offers"
        )


    offer.status = "Accepted"

    offer.save()


    messages.success(
        request,
        "Hiring offer accepted successfully."
    )


    return redirect(
        "my_hiring_offers"
    )


# =========================================================
# REJECT HIRING OFFER
# =========================================================

def reject_hiring_offer(
    request,
    offer_id
):

    if request.method != "POST":

        return redirect(
            "my_hiring_offers"
        )


    student_id = request.session.get(
        "student_id"
    )

    if not student_id:
        return redirect(
            "student_login"
        )


    student = get_object_or_404(
        Student,
        id=student_id
    )


    offer = get_object_or_404(
        HiringOffer,
        id=offer_id,
        student_email__iexact=student.email.strip()
    )


    # Only Offered/Pending offer can be rejected
    if offer.status not in [
        "Pending",
        "Offered"
    ]:

        messages.warning(
            request,
            "This hiring offer cannot be rejected."
        )

        return redirect(
            "my_hiring_offers"
        )


    offer.status = "Rejected"

    offer.save()


    messages.success(
        request,
        "Hiring offer rejected."
    )


    return redirect(
        "my_hiring_offers"
    )