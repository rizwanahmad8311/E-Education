from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Course_media,  Enrollment, TimeTable, Course,Class


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}),error_messages={'required':'First Name is required.',})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Last Name is required.',})
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),error_messages={'required':'Email is required.',})

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password')
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'username':{
                'required':'Username is required.'
            },
            'password': {
                'required': 'Password is required.',
                'min_length': 'Password must be at least %(limit_value)d characters long.',
            },
        }

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}),error_messages={'required':'First Name is required.',})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Last Name is required.',})
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),error_messages={'required':'Email is required.',})
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            # 'password': forms.PasswordInput(),
        }
        error_messages = {
            'username':{
                'required':'Username is required.'
            },
            # 'password':{
            #     'required':False
            # },
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'placeholder': 'Username'}),error_messages={'required':'Username is required.',})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),error_messages={'required':'Password is required.',})


class Course_mediaForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control '}),error_messages={'required':'Title is required.',})
    file = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}),error_messages={'required':'File is required.',})
    class Meta:
        model = Course_media
        fields = ('title','file')

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'
        # fields = ('title','file')

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ('day','start_time','end_time')
        widgets = {
            'day': forms.Select(attrs={'class':'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time','class':'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time','class':'form-control'})
        }


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_title']
        widgets = {
            'course_title': forms.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'course_title':{
                'required':'Course Title is required.'
            }
        }

class AddClassForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control '}),error_messages={'required':'Title is required.',})
    class Meta:
        model = Class
        fields = ['class_title','section','batch','session']
        widgets = {
            'class_title': forms.Select(attrs={'class':'form-control'}),
            'section': forms.Select(attrs={'class':'form-control'}),
            'batch': forms.Select(attrs={'class':'form-control'}),
            'session': forms.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'class_title':{
                'required':'Class Title is required.'
            },
            'section':{
                'required':'Section is required.'
            },
            'batch':{
                'required':'Batch is required.'
            },
            'session':{
                'required':'Session is required.'
            }
        }