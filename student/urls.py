from django.urls import path
from student import views

urlpatterns = [
    
    path('signup/', views.SignUp_View.as_view() ,name="st-signup"),
    path('login/', views.Login_View.as_view() ,name="st-login"),
    path('forgot-password/', views.Forgot_Password_View.as_view() ,name="st-forgot-password"),
    path('forgot-password/<uuid>/', views.Forgot_Link_View.as_view() ,name="st-forgotlink"),
    path('myprofile/', views.my_profile ,name="st-myprofile"),
    path('courses/', views.courses ,name="courses"),
    path('courses/apply/<str:id>/', views.apply_enrollment ,name="st-courses-apply"),
    path('myenrollments/', views.myenrollments ,name="myenrollments"),
    path('mytimetable/', views.mytimetable ,name="mytimetable"),
    # path('myattendance/', views.myattendance ,name="myattendance"),
    path('logout/', views.user_logout ,name="st-logout"),

    path("contacts/", views.contacts, name="st-contacts"),
    path("contact-chat/<int:receiver_id>/", views.contact_chat, name="st-contact-chat"),


]
