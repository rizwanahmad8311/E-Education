from django.contrib import admin
from .models import IsStudent, Chat, Group, Progress

admin.site.site_header = "E-Education ADMIN"
admin.site.site_title = "E-Education ADMIN PORTAL"
admin.site.index_title = "WELCOME TO E-Education ADMIN PORTAL"


@admin.register(IsStudent)
class IsStudentAdmin(admin.ModelAdmin):
    list_display = ['id','stu_id','is_student','account_status']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','content','time','user','group']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id','name','admin','participants_group']

    def participants_group(self,obj):
        return ", ".join([participant.username for participant in obj.participants.all()])

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['id','user','course_media','downloaded','downloaded_date']








