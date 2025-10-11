from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relatorios/', include('reports.urls')),
    path('painel-admin/', include('core.urls')),
    path('', include('ebd.urls')),
]