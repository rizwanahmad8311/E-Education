from django.contrib import admin
from .models import IsProfessor, Class, Course, AssignProfessor, Course_media, Enrollment, Forgot_Password, TimeTable
# Register your models here.

@admin.register(IsProfessor)
class IsProfessorAdmin(admin.ModelAdmin):
    list_display = ['id','prf_id','is_professor','account_status']

@admin.register(Forgot_Password)
class Forgot_PasswordAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','uuid',]
    

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id','title','section','batch','session']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','title']

@admin.register(AssignProfessor)
class AssignProfessorAdmin(admin.ModelAdmin):
    list_display = ['id','prf_id','class_id','course_id','status']

@admin.register(Course_media)
class Course_mediaAdmin(admin.ModelAdmin):
    list_display = ['id','prf_id','course_id','title','file','created_at']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id','stu_id','assign_professor_id','status']

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['id','prf_id','assign_professor_id','day','start_time','end_time']