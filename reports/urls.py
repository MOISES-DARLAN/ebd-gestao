from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.attendance_history, name='history'),
    path('chamada/<int:chamada_id>/', views.chamada_detalhes, name='details'),
]