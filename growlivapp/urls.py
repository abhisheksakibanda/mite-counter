from django.urls import path

from . import views
from .views import BusinessLoginView, BusinessRegisterView

app_name = 'growlivapp'

urlpatterns = [
    # path for the home page
    path('', views.home, name='home'),

    # path for the login and registration pages
    path('login/', BusinessLoginView.as_view(), name='login'),
    path('signup/', BusinessRegisterView.as_view(), name='signup'),

    path('upload/', views.upload_video, name='upload'),
    path('profile/', views.profile, name='profile'),
    path('scan_detail/', views.scan_detail_page, name='scan_detail_page'),

    # path for login related pages
    path('instruction/', views.instructions, name='instruction'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_user, name='logout_user'),
]
