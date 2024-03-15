from django.urls import path

from . import views

app_name = 'counterapp'

urlpatterns = [
    path('predict/', views.predict, name='predict'),
]
