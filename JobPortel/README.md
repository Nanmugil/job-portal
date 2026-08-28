# 🚀 JobPortal - Django Job & Internship Portal

A web-based **Job and Internship Portal** developed using **Python and Django**.

JobPortal provides a platform where students can search and apply for jobs and internships, while employers can post job opportunities, manage applications, and send hiring offers to selected candidates.

---

## 📌 Project Overview

JobPortal is designed to connect **students/job seekers** with **employers** through a simple and user-friendly web application.

### 👨‍🎓 Students can:

- Register and login
- Create and edit their profile
- Add skills, qualification and location
- Upload resume
- View available jobs
- View internship opportunities
- Search jobs by title, company or skills
- Filter jobs by location
- Apply for jobs
- View submitted applications
- Track application status
- Receive hiring offers
- Accept or reject hiring offers

### 🏢 Employers can:

- Register and login
- Create and edit company profile
- Post jobs and internships
- View posted jobs
- Edit jobs
- Delete jobs
- View applicants
- Accept applications
- Reject applications
- Send hiring offers
- Track hiring offer status
- View hiring offer statistics through the dashboard

---

## ✨ Main Features

### 🔐 Authentication

- Student Registration
- Student Login
- Student Logout
- Employer Registration
- Employer Login
- Employer Logout
- Session-based authentication

### 👨‍🎓 Student Module

- Student Dashboard
- Student Profile
- Edit Profile
- Resume Upload
- Job Search
- Job Filtering
- Internship Listing
- Job Application
- My Applications
- Hiring Offers
- Accept Hiring Offer
- Reject Hiring Offer

### 🏢 Employer Module

- Employer Dashboard
- Employer Profile
- Edit Company Profile
- Post Job
- My Jobs
- Edit Job
- Delete Job
- View Applicants
- Accept Application
- Reject Application
- Send Hiring Offer
- Employer Hiring Offers

### 📊 Dashboard

The employer dashboard provides statistics such as:

- Total Jobs
- Total Applicants
- Accepted Applications
- Rejected Applications
- Pending Applications
- Total Hiring Offers
- Accepted Hiring Offers
- Rejected Hiring Offers
- Pending Hiring Offers

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Django | Web Framework |
| HTML5 | Web Page Structure |
| CSS3 | Styling & Responsive Design |
| JavaScript | Client-side Interaction |
| SQLite3 | Database |
| Git | Version Control |
| GitHub | Project Hosting |

---

## 📂 Project Structure

```text
JobPortel/
│
├── manage.py
├── db.sqlite3
│
├── jobportel/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── students/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── employers/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── jobs/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── dashboard/
│   └── ...
│
├── static/
│   └── css/
│
├── media/
│   └── resumes/
│
├── requirements.txt
├── .gitignore
└── README.md