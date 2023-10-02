from django.urls import path
from professor import views

urlpatterns = [
    
    path('', views.home ,name="prf-home"),
    path('signup/', views.SignUp_View.as_view() ,name="prf-signup"),
    path('login/', views.Login_View.as_view() ,name="prf-login"),
    path('forgot-password/', views.Forgot_Password_View.as_view() ,name="prf-forgot-password"),
    path('forgot-password/<uuid>/', views.Forgot_Link_View.as_view() ,name="prf-forgotlink"),
    path('my-profile/', views.my_profile ,name="prf-myprofile"),
    path('my-profile/edit', views.my_profile_edit ,name="prf-myprofile-edit"),
    path('add-course/', views.add_course ,name="add-course"),
    path('my-courses/', views.My_Courses_View.as_view() ,name="prf-mycourses"),
    path('my-course-lectures/<str:cid>', views.my_course_lectures ,name="prf-mycourse-lectures"),
    path('delete-course-lecture/<str:cid>/<str:lecture_id>', views.delete_course_lecture ,name="prf-delete-course-lecture"),
    path('prf-attendance/', views.attendance ,name="prf-attendance"),
    path('prf-take-attendance/<int:cid>/', views.take_attendance ,name="prf-take-attendance"),
    path('lecture-time/<str:cid>', views.Lecture_Time_View.as_view() ,name="lecture-time"),
    path('delete-lecture-time/<str:cid>/<str:lid>', views.delete_lecture_time ,name="delete-lecture-time"),
    path('logout/', views.user_logout ,name="prf-logout"),

    
    path("contacts/", views.contacts, name="prf-contacts"),
    path("contact-chat/<int:receiver_id>/", views.contact_chat, name="prf-contact-chat"),



]
