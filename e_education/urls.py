
from django.contrib import admin
from django.urls import path,include
from student import views
from .settings import MEDIA_ROOT,MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('st/',include('student.urls')),
    path('prf/',include('professor.urls')),

    path('', views.home ,name="home"),

    



]
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
