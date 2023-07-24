from django.contrib import admin
from django.urls import path,include
from myapp import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login_view'),
    path('main/', views.main, name='main'),    
    path('signup/', views.signup, name='signup'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'), 
    path('logout/', views.logout_user, name='logout'),

]