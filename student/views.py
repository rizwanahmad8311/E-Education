from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .models import IsStudent,Group,Chat
from professor.models import AssignProfessor, Enrollment, Course_media,Forgot_Password, IsProfessor, TimeTable
from django.contrib.auth.hashers import make_password
import uuid
from django.contrib.auth.decorators import login_required

class SignUp_View(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, 'student/signup.html', {'pgname': 'Signup', 'form': form, })

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                if User.objects.get(email=email):
                    return render(request, 'student/signup.html', {'pgname': 'Signup', 'form': form, 'error': 'A user with that email already exists.'})
            except:
                try:
                    if User.objects.get(username=username):
                        return render(request, 'student/signup.html', {'pgname': 'Signup', 'form': form, 'error': 'A user with that username already exists.'})
                except:
                    if len(password) < 8:
                        return render(request, 'student/signup.html', {'pgname': 'Signup', 'form': form, 'error': 'Password must be 8 characters or greater.'})
                    else:
                        hashed_password = make_password(password)
                        frm = form.save(commit=False)
                        frm.password = hashed_password
                        frm.save()
                        is_student = IsStudent(stu_id=frm,is_student=True)
                        is_student.save()
                        form = forms.SignUpForm()
                        return render(request, 'student/signup.html', {'pgname': 'Signup', 'form': form, 'success': 'Account Created Successfully!'})
        else:
            return render(request, 'student/signup.html', {'pgname': 'Signup', 'form': form })


class Login_View(View):
    def get(self, request):
        return render(request, 'student/login.html', {'pgname': 'Login' })

    def post(self, request):
        obj = request.POST
        username = obj.get('username')
        password = obj.get('password')
        try:
            user = User.objects.get(username=username)
            is_student = IsStudent.objects.get(stu_id=user)
            if is_student.account_status:
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'student/login.html', {'pgname': 'Login', 'error': 'Incorrect username or password', 'username': username})
            else:
                return render(request, 'student/login.html', {'pgname': 'Login', 'error': 'Account is not Approved by Authorities.', 'username': username})
        except:
            return render(request, 'student/login.html', {'pgname': 'Login', 'error': 'Incorrect username or password', 'username': username})



class Forgot_Password_View(View):
    def get(self, request):
        return render(request, 'student/forgotpassword.html', {'pgname': 'Forgot Password',})

    def post(self, request):
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except:
                user = False
            if user:
                try:
                    already = Forgot_Password.objects.get(user_id=user)
                except:
                    already = False
                if already:
                    return render(request, 'student/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'error': 'Link to create new password has already been sent to your email.',})
                else:
                    email_uuid = str(uuid.uuid4())
                    link = Forgot_Password(
                        user_id=user, uuid=email_uuid)
                    link.save()
                    sent = self.sendmail(email, email_uuid)
                    if sent:
                        return render(request, 'student/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'success': 'Link to create new password has been sent to your email.',})
                    else:
                        return render(request, 'student/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'error': 'We are facing some issue. Please Try again later.',})
            else:
                return render(request, 'student/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'error': 'Incorrect Email',})
        else:
            return render(request, 'student/forgotpassword.html', {'pgname': 'Forgot Password', 'error': 'Email is required',})

    def sendmail(self, email, email_uuid,):
        sent = False

        from email.message import EmailMessage
        import ssl
        import smtplib

        # Authentication
        sender_email = "fypranking@gmail.com"
        sender_email_password = 'hspbqxkbpwabjvhx'
        receiver_email = email

        subject = "E-Education Password Reset"

        body = f"""Dear User,
        \n This is an Password Reset mail from E-Education.Verify your email by clicking this link http://127.0.0.1:8000/st/forgot-password/{email_uuid}
        \n Once you click this link you will be redirected to the new password creation page
        \n Note: This link is one time link after one attempt link will be expired.
        \n If you face any issue,then write to fypranking@gmail.com
        \n\n Best regards,
        \n E-Education
        """

        em = EmailMessage()

        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_email_password)
            smtp.sendmail(sender_email, receiver_email, em.as_string())
            sent = True

        return sent


class Forgot_Link_View(View):
    def get(self, request, uuid=None):
        try:
            Forgot_Password.objects.get(uuid=uuid)
            print(Forgot_Password.objects.get(uuid=uuid))
            return render(request, 'student/forgotlink.html', {'pgname': 'Forgot Password',})
        except:
            return redirect('page-not-found')

    def post(self, request, uuid=None):
        try:
            uuid_db = Forgot_Password.objects.get(uuid=uuid)
            newpassword = request.POST.get('password')
            if newpassword:
                if len(newpassword) < 8:
                    return render(request, 'student/forgotlink.html', {'pgname': 'Forgot Password', 'error': 'Password must be 8 characters or greater.',})
                else:
                    User.objects.filter(id=uuid_db.user_id.id).update(
                        password=make_password(newpassword))
                    uuid_db.delete()
                    return render(request, 'student/forgotlink.html', {'pgname': 'Forgot Password', 'success': 'Password has been updated Successfully',})
            else:
                return render(request, 'student/forgotlink.html', {'pgname': 'Forgot Password', 'error': 'Password is required',})
        except:
            return redirect('page-not-found')



def my_profile(request):
    user_data = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = forms.ProfileUpdateForm(request.POST, instance=user_data)
        if form.is_valid():
            form.save()
            login(request, user_data)
            data = {
                'user': user_data,
                'myprofile': True,
                'pgname': 'My Profile',
                'logged': True,
                'form': form,
                'success': 'Profile has been updated',
            }
            return render(request, 'student/myprofile.html', data)
    else:
        form = forms.ProfileUpdateForm(instance=user_data)
        data = {
            'user': user_data,
            'myprofile': True,
            'pgname': 'My Profile',
            'logged': True,
            'form': form,
        }
    return render(request, 'student/myprofile.html', data)


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        data = {
            'user': user_db,
            'home': True,
            'pgname': 'Home',
            'logged': True,
        }
        try:
            IsStudent.objects.get(stu_id=user_db)
            return render(request, 'student/index.html', data)
        except:
            return render(request, 'professor/index.html', data)
    else:
        return redirect('st-login')

def courses(request):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        mycourses = Enrollment.objects.filter(stu_id=user_db).values_list('assign_professor_id__course_id', flat=True)
        enrollments = Enrollment.objects.all()
        courses = AssignProfessor.objects.filter(status=True)
        data = {
            'user': user_db,
            'courses': True,
            'pgname': 'Courses',
            'logged': True,
            'courses_list':courses,
            'my_courses':mycourses,
            'enrollments':enrollments
        }
        return render(request,'student/courses.html',data)
    else:
        return redirect('st-login')
    
def apply_enrollment(request,id):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        course = AssignProfessor.objects.get(id=id)
        try:
            Enrollment.objects.get(stu_id=user_db,assign_professor_id=course)
            return redirect('courses')
        except:
            obj = Enrollment(stu_id=user_db,assign_professor_id=course)
            obj.save()
            return redirect('courses')
    else:
        return redirect('st-login')
    


def myenrollments(request):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        enrollments = Enrollment.objects.filter(stu_id=user_db)
        course_media = Course_media.objects.all()
        data = {
            'user': user_db,
            'myenrollments': True,
            'pgname': 'My Enrollments',
            'logged': True,
            'enrollments':enrollments,
            'course_media':course_media
        }
        return render(request,'student/myenrollments.html',data)
    else:
        return redirect('st-login')


# def myattendance(request):
#     if request.user.is_authenticated:
#         user_db = User.objects.get(pk=request.user.id)
#         enrollments = Enrollment.objects.filter(stu_id=user_db)
#         course_media = Course_media.objects.all()
#         data = {
#             'user': user_db,
#             'myattendance': True,
#             'pgname': 'My Attendance',
#             'logged': True,
#             'enrollments':enrollments,
#             'course_media':course_media
#         }
#         return render(request,'student/myattendance.html',data)
#     else:
#         return redirect('st-login')


@login_required(login_url="/signin/")
def contacts(request):
    if request.method == 'GET':
        user_db = User.objects.get(pk=request.user.id)
        # contacts = IsProfessor.objects.filter(is_professor=True,account_status=True)
        contacts = Enrollment.objects.filter(stu_id=user_db)
        data = {
            'user': user_db,
            'contacts': True,
            'pgname': 'Contacts',
            'logged': True,
            'contacts':contacts
        }
        return render(request, 'student/contacts.html', data)
    
@login_required(login_url="/signin/")
def contact_chat(request,receiver_id):
    groupname = f"{request.user.id}_{receiver_id}"
    group = Group.objects.filter(name=groupname).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group.id).order_by('time')
    else:
        groupname = f"{receiver_id}_{request.user.id}"
        group = Group.objects.filter(name=groupname).first()
        if group:
            chats = Chat.objects.filter(group=group.id).order_by('time')
        else:
            newgroup = Group(name=groupname)
            newgroup.save()
            newgroup.participants.add(request.user)
            newgroup.participants.add(receiver_id)
    user_db = User.objects.get(pk=request.user.id)
    data = {
            'user': user_db,
            'contacts': True,
            'pgname': 'Chat',
            'logged': True,
            'group_name':groupname,
            'chats':chats,
        }
    return render(request,'student/chat.html',data)
  


def mytimetable(request):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        enrollments = Enrollment.objects.filter(stu_id=user_db)
        timetable = TimeTable.objects.all()
        data = {
            'user': user_db,
            'mytimetable': True,
            'pgname': 'My TimeTable',
            'logged': True,
            'enrollments':enrollments,
            'timetable':timetable
        }
        return render(request,'student/mytimetable.html',data)
    else:
        return redirect('st-login')

