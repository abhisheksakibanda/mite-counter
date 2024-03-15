from django.urls import path

from . import views

app_name = 'growlivapp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('upload-photos/', views.upload_photos, name='upload_photos'),
    # Add other URLs as needed
]
