from django.db import models
from django.contrib.auth.models import User

class IsProfessor(models.Model):
    prf_id = models.ForeignKey(User,on_delete=models.CASCADE)
    account_status = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)


class Class(models.Model):
    TITLE_CHOICES = (
        ('Information Technology', 'Information Technology'),
        ('Software Engineering', 'Software Engineering'),
        ('Computer Science', 'Computer Science'),
        ('Computer Engineering', 'Computer Engineering'),
    )
    class_title = models.CharField(max_length=200,choices=TITLE_CHOICES)
    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    section = models.CharField(max_length=200,choices=SECTION_CHOICES)
    BATCH_CHOICES = (
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
    )
    batch = models.CharField(max_length=200,choices=BATCH_CHOICES)
    SESSION_CHOICES = (
        ('Spring', 'Spring'),
        ('Fall', 'Fall'),
    )
    session = models.CharField(max_length=20,choices=SESSION_CHOICES)

    def __str__(self):
        return self.class_title
    

class Course(models.Model):
    COURSE_CHOICES = (
        ('Programming Fundamentals', 'Programming Fundamentals'),
        ('Islamic Studies', 'Islamic Studies'),
        ('Software Engineering', 'Software Engineering'),
    )
    course_title = models.CharField(max_length=100,choices=COURSE_CHOICES)

    def __str__(self):
        return self.course_title
    

class Forgot_Password(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=250)


class AssignProfessor(models.Model):
    prf_id = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'groups__name': 'Professors'})
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course_id.course_title}------{self.prf_id.first_name}  {self.prf_id.last_name}"
    

class Course_media(models.Model):
    prf_id = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_lectures/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    stu_id = models.ForeignKey(User,on_delete=models.CASCADE)
    assign_professor_id = models.ForeignKey(AssignProfessor,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class TimeTable(models.Model):
    prf_id = models.ForeignKey(User,on_delete=models.CASCADE)
    assign_professor_id = models.ForeignKey(AssignProfessor,on_delete=models.CASCADE)
    TITLE_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    day = models.CharField(max_length=20,choices=TITLE_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

  