from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .models import IsProfessor, AssignProfessor, Course_media, Enrollment, Course, Forgot_Password, TimeTable
from django.contrib.auth.hashers import make_password
import uuid
from django.contrib.auth.decorators import login_required
from student.models import IsStudent,Group,Chat

class SignUp_View(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, 'professor/signup.html', {'pgname': 'Signup', 'form': form, })

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                if User.objects.get(email=email):
                    return render(request, 'professor/signup.html', {'pgname': 'Signup', 'form': form, 'error': 'A user with that email already exists.'})
            except:
                try:
                    if User.objects.get(username=username):
                        return render(request, 'professor/signup.html', {'pgname': 'Signup', 'form': form, 'error': 'A user with that username already exists.'})
                except:
                    if len(password) < 8:
                        return render(request, 'professor/signup.html', {'pgname': 'Signup', 'form': form, 'error': 'Password must be 8 characters or greater.'})
                    else:
                        hashed_password = make_password(password)
                        frm = form.save(commit=False)
                        frm.password = hashed_password
                        frm.save()
                        is_professor = IsProfessor(
                            prf_id=frm, is_professor=True)
                        is_professor.save()
                        form = forms.SignUpForm()
                        return render(request, 'professor/signup.html', {'pgname': 'Signup', 'form': form, 'success': 'Account Created Successfully!'})
        else:
            return render(request, 'professor/signup.html', {'pgname': 'Signup', 'form': form})


class Login_View(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('prf-home')
        else:
            return render(request, 'professor/login.html', {'pgname': 'Login'})

    def post(self, request):
        obj = request.POST
        username = obj.get('username')
        password = obj.get('password')
        try:
            user = User.objects.get(username=username)
            is_professor = IsProfessor.objects.get(prf_id=user)
            if is_professor.account_status:
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user:
                    login(request, user)
                    return redirect('prf-home')
                else:
                    return render(request, 'professor/login.html', {'pgname': 'Login', 'error': 'Incorrect username or Password', 'username': username})
            else:
                return render(request, 'professor/login.html', {'pgname': 'Login', 'error': 'Account is not Approved by Authorities.', 'username': username})
        except:
            return render(request, 'professor/login.html', {'pgname': 'Login', 'error': 'Incorrect username or Password', 'username': username})

class Forgot_Password_View(View):
    def get(self, request):
        return render(request, 'professor/forgotpassword.html', {'pgname': 'Forgot Password',})

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
                    return render(request, 'professor/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'error': 'Link to create new password has already been sent to your email.',})
                else:
                    email_uuid = str(uuid.uuid4())
                    link = Forgot_Password(
                        user_id=user, uuid=email_uuid)
                    link.save()
                    sent = self.sendmail(email, email_uuid)
                    if sent:
                        return render(request, 'professor/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'success': 'Link to create new password has been sent to your email.',})
                    else:
                        return render(request, 'professor/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'error': 'We are facing some issue. Please Try again later.',})
            else:
                return render(request, 'professor/forgotpassword.html', {'pgname': 'Forgot Password', 'email': email, 'error': 'Incorrect Email',})
        else:
            return render(request, 'professor/forgotpassword.html', {'pgname': 'Forgot Password', 'error': 'Email is required',})

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
        \n This is an Password Reset mail from E-Education Portal.Verify your email by clicking this link http://127.0.0.1:8000/prf/forgot-password/{email_uuid}
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
            return render(request, 'professor/forgotlink.html', {'pgname': 'Forgot Password',})
        except:
            return redirect('page-not-found')

    def post(self, request, uuid=None):
        try:
            uuid_db = Forgot_Password.objects.get(uuid=uuid)
            newpassword = request.POST.get('password')
            if newpassword:
                if len(newpassword) < 8:
                    return render(request, 'professor/forgotlink.html', {'pgname': 'Forgot Password', 'error': 'Password must be 8 characters or greater.',})
                else:
                    User.objects.filter(id=uuid_db.user_id.id).update(
                        password=make_password(newpassword))
                    uuid_db.delete()
                    return render(request, 'professor/forgotlink.html', {'pgname': 'Forgot Password', 'success': 'Password has been updated Successfully',})
            else:
                return render(request, 'professor/forgotlink.html', {'pgname': 'Forgot Password', 'error': 'Password is required',})
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
            return render(request, 'professor/myprofile.html', data)
        else:
            data = {
                'user': user_data,
                'myprofile': True,
                'pgname': 'My Profile',
                'logged': True,
                'form': form,
                'error': 'A user with that username already exists.',
            }
            return render(request, 'professor/myprofile.html', data)
    else:
        form = forms.ProfileUpdateForm(instance=user_data)
        data = {
            'user': user_data,
            'myprofile': True,
            'pgname': 'My Profile',
            'logged': True,
            'form': form,
        }
    return render(request, 'professor/myprofile.html', data)


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
        return render(request, 'professor/index.html', data)
    else:
        return redirect('prf-login')


class My_Courses_View(View):
    def get(self,request):
        if request.user.is_authenticated:
            user_db = User.objects.get(pk=request.user.id)
            my_courses = AssignProfessor.objects.filter(prf_id=user_db,status=True)
            form = forms.Course_mediaForm()
            enrollment = []
            for i in my_courses:
                data = {
                'enrollment_count' : Enrollment.objects.filter(assign_professor_id=i.id,status=True).count(),
                'course_id':i
                }
                enrollment.append(data)
            data = {
                'user': user_db,
                'courses': True,
                'pgname': 'Courses',
                'logged': True,
                'mycourses':my_courses,
                'form':form,
                'enrollment':enrollment
            }
            return render(request, 'professor/mycourses.html', data)
        else:
            return redirect('prf-login')
        
    def post(self,request):
        if request.user.is_authenticated:
            form = forms.Course_mediaForm(request.POST, request.FILES)
            user_db = User.objects.get(pk=request.user.id)
            if form.is_valid():
                course_id = request.POST.get('course_id')
                frm = form.save(commit=False)
                course_db = Course.objects.get(id=course_id)
                frm.prf_id = user_db
                frm.course_id = course_db
                frm.save()
                return redirect('prf-mycourses')
            else:
                print(form.errors)
                return render(request, 'professor/mycourses.html')
        else:
            return redirect('prf-login')

    
def my_course_lectures(request,cid):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        my_course_lectures = Course_media.objects.filter(course_id=cid,prf_id=user_db)
        data = {
            'user': user_db,
            'course_lectures': True,
            'pgname': 'Course Lectures',
            'logged': True,
            'my_course_lectures':my_course_lectures,
        }
        return render(request, 'professor/course-folder.html', data)
    else:
        return redirect('prf-login')
    

def delete_course_lecture(request,cid,lecture_id):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        delete_course_lecture = Course_media.objects.get(id=lecture_id,prf_id=user_db)
        delete_course_lecture.delete()
        return redirect('prf-mycourse-lectures', cid)
    else:
        return redirect('prf-login')
    
    
def attendance(request):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        my_courses = AssignProfessor.objects.filter(prf_id=user_db,status=True)
        enrollment = []
        for i in my_courses:
            data = {
            'enrollment_count' : Enrollment.objects.filter(assign_professor_id=i.id,status=True).count(),
            'enrollment' : Enrollment.objects.filter(assign_professor_id=i.id,status=True),
            'course_id':i
            }
            enrollment.append(data)
        data = {
            'user': user_db,
            'attendance': True,
            'pgname': 'Attendance',
            'logged': True,
            'mycourses':my_courses,
            'enrollment':enrollment
        }
        return render(request, 'professor/attendance.html', data)
    else:
        return redirect('prf-login')
    
def take_attendance(request,cid):
    if request.method == 'POST':
        print(request.POST.get('is_present'))
        return redirect('prf-attendance')
    else:
        if request.user.is_authenticated:
            print(forms.AttendanceForm())
            user_db = User.objects.get(pk=request.user.id)
            data = {
                'user': user_db,
                'attendance': True,
                'pgname': 'Attendance',
                'logged': True,
                'enrollment' : Enrollment.objects.filter(assign_professor_id__prf_id=user_db,assign_professor_id__course_id__id=cid,status=True),
            }
            return render(request, 'professor/take-attendance.html', data)
        else:
            return redirect('prf-login')
        

@login_required(login_url="/signin/")
def contacts(request):
    if request.method == 'GET':
        user_db = User.objects.get(pk=request.user.id)
        contacts = IsStudent.objects.filter(is_student=True,account_status=True)
        print(user_db)
        print(contacts)
        data = {
            'user': user_db,
            'contacts': True,
            'pgname': 'Contacts',
            'logged': True,
            'contacts':contacts
        }
        return render(request, 'professor/contacts.html', data)
    
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
    return render(request,'professor/chat.html',data)
  

class Lecture_Time_View(View):
    def get(self,request,cid):
        if request.user.is_authenticated:
            user_db = User.objects.get(pk=request.user.id)
            try:
                lecture_time = TimeTable.objects.get(assign_professor_id__course_id__id=cid,prf_id=user_db)
                data = {
                    'user': user_db,
                    'course_lectures': True,
                    'pgname': 'Lecture Time Table',
                    'logged': True,
                    'lecture_time':lecture_time,
                }
                return render(request, 'professor/time_table.html', data)
            except:
                data = {
                    'user': user_db,
                    'course_lectures': True,
                    'pgname': 'Lecture Time Table',
                    'logged': True,
                    'form':forms.TimeTableForm()
                }
                return render(request, 'professor/time_table.html', data)

        else:
            return redirect('prf-login')
        
    def post(self,request,cid):
        if request.user.is_authenticated:
            form = forms.TimeTableForm(request.POST)
            if form.is_valid():
                user_db = User.objects.get(pk=request.user.id)
                assign_professor_id_db = AssignProfessor.objects.get(course_id__id=cid)
                frm = form.save(commit=False)
                frm.prf_id = user_db
                frm.assign_professor_id = assign_professor_id_db
                frm.save()
                return redirect('lecture-time',cid)
        else:
            return redirect('prf-login')
    

def delete_lecture_time(request,cid,lid):
    if request.user.is_authenticated:
        user_db = User.objects.get(pk=request.user.id)
        delete_lecture_time = TimeTable.objects.get(id=lid,prf_id=user_db)
        delete_lecture_time.delete()
        return redirect('lecture-time', cid)
    else:
        return redirect('prf-login')
  