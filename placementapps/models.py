
from django.db import models
from django.utils.text import slugify
from django.shortcuts import redirect, render

  
class tbl_student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    roll_no = models.CharField(max_length=50)  # Roll number field
    reg_no = models.CharField(max_length=50)  # Registration number field
    student_id = models.CharField(max_length=50)  # Student ID field
    name = models.CharField(max_length=200)  # Student name field
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)  # Gender field
    student_email = models.EmailField()  # Student email field
    student_phone = models.CharField(max_length=10)  # Student phone field
    parent_phone = models.CharField(max_length=10)  # Parent phone field
    address = models.TextField(max_length=128)  # Address field
    
    date_of_birth = models.DateField(null=True, blank=True)  
    password = models.CharField(max_length=128) 
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    department = models.ForeignKey('tbl_department', on_delete=models.SET_NULL, null=True, blank=True) 
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')  
    year = models.PositiveIntegerField(null=True, blank=True) 
    supply = models.PositiveIntegerField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Resume file field
    pancard_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Passcard number field
    batch = models.CharField(max_length=100, null=True, blank=True)  # Batch field
    
    def __str__(self):
        return self.name

from django.db import models



    
class tbl_admin(models.Model):
    password = models.CharField(max_length=200)
    email = models.EmailField()


from django.db import models
class tbl_department(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.icon:
            icon_mapping = {
                "English": "fa-book",
                "Malayalam": "fa-book-open",
                "Mathematics": "fa-calculator",
                "Statistics": "fa-chart-line",
                "History": "fa-history",
                "Botany": "fa-leaf",
                "Computer Science": "fa-laptop-code",
                "Physics": "fa-atom",
                "Chemistry": "fa-flask",
                "Zoology": "fa-paw",
                "Social Work": "fa-users",
                "Home Science": "fa-utensils",
                "Psychology": "fa-brain",
                "Commerce": "fa-money-bill-wave",
                "Economics": "fa-chart-pie",
                "Sociology": "fa-users",  
            }
            self.icon = icon_mapping.get(self.name, "fa-building")
        if not self.slug:
            self.slug = slugify(self.name)

        super(tbl_department, self).save(*args, **kwargs)


class Job(models.Model):
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/')
    job_type = models.CharField(
        max_length=10,
        choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time')],
        default='full-time',
    )
    description =models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    
    # Automatically set the current date when a new job is created
    date = models.DateField(auto_now_add=True)
    
    department = models.ForeignKey(
        'tbl_department', 
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    responsibilities = models.TextField(max_length=500)
    qualifications = models.TextField(max_length=500)
    vacancy = models.PositiveIntegerField(default=1)
        
    # New field for Passout Year
    passoutyear = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.title} - {self.department.name} - ${self.salary}"

from datetime import date
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey('tbl_student', on_delete=models.CASCADE)  # User is the student
    job = models.ForeignKey('Job', on_delete=models.CASCADE)  # The job that the student is applying for
    applied_on = models.DateField(default=date.today)  # Date of application
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.name} applied for {self.job.title} on {self.applied_on}"
    
class TrainingSession(models.Model):
    session_name = models.CharField(max_length=255)
    description = models.TextField()
    trainer_name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    time = models.TimeField()
    training_dates = models.JSONField()

class Course(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(tbl_department, on_delete=models.CASCADE, related_name='courses')
    def __str__(self):
        return self.name

  
    
   
from django.db import models
from django.contrib.auth.models import User
from datetime import date

from datetime import datetime

class SessionApplication(models.Model):
    user = models.ForeignKey(tbl_student, on_delete=models.CASCADE)
    session = models.ForeignKey('TrainingSession', on_delete=models.CASCADE)
    applied_on = models.DateTimeField(default=datetime.now)  # Use DateTimeField for date and time

    def __str__(self):
        return f"{self.user.username} applied for {self.session.session_name} on {self.applied_on}"



class tbl_tutor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tutor_images/', blank=True, null=True)
    department = models.ForeignKey(tbl_department, on_delete=models.CASCADE, related_name='tutors')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tutors')
    batch = models.CharField(max_length=20)  # E.g., "2022-2024"
    status = models.CharField(max_length=100, default='pending')

    def __str__(self):
        return self.name
    
    

from django.db import models
from django.db import models
from django.utils.timezone import now

class StudentNotification(models.Model):
    student = models.ForeignKey('tbl_student', on_delete=models.CASCADE, related_name='notifications')
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)  # Track if the notification has been read

    def __str__(self):
        return f"Notification for {self.student.name} - {self.job.title}"

    
    
    
from django.db import models
class TutorNotification(models.Model):
    tutor = models.ForeignKey(
        tbl_tutor, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.TextField()  # Notification message
    is_read = models.BooleanField(default=False)  # To track read/unread status
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the current date and time when created

    def __str__(self):
        return f"Notification for {self.tutor.name} - Job: {self.job.title}"
