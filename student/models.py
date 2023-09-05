from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class IsStudent(models.Model):
    stu_id = models.ForeignKey(User,on_delete=models.CASCADE)
    account_status = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class Chat(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey('Group',on_delete=models.CASCADE)

class Group(models.Model):
    admin = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=400)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.name

