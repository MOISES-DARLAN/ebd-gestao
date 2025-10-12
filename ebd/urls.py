from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ebd'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='ebd/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home_page, name='home'),
    
    path('dashboard/', views.dashboard, name='dashboard'),

    path('turma/<int:turma_id>/', views.turma_dashboard, name='turma_dashboard'),
    path('turma/<int:turma_id>/acesso/', views.acesso_turma, name='acesso_turma'),
    path('turma/<int:turma_id>/chamada/', views.chamada, name='chamada'),
    
    path('turma/<int:turma_id>/alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),
    path('turma/<int:turma_id>/aluno/adicionar/', views.aluno_create, name='aluno_create'),
    path('turma/<int:turma_id>/aluno/<int:aluno_id>/editar/', views.aluno_update, name='aluno_update'),
    path('turma/<int:turma_id>/aluno/<int:aluno_id>/excluir/', views.aluno_delete, name='aluno_delete'),
]