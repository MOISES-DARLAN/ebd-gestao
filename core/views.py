from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from ebd.models import Turma, Aluno, Chamada, RegistroAlunoChamada
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum, Count

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
def admin_dashboard(request):
    hoje = date.today()

    # Cards de Estatísticas Gerais
    total_turmas = Turma.objects.count()
    total_alunos = Aluno.objects.count()
    total_professores = User.objects.filter(is_staff=False).count()

    # Estatísticas do Dia (última chamada)
    chamadas_de_hoje = Chamada.objects.filter(data=hoje)
    presentes_hoje = RegistroAlunoChamada.objects.filter(chamada__in=chamadas_de_hoje, presente=True).count()
    oferta_hoje = chamadas_de_hoje.aggregate(total=Sum('oferta_do_dia'))['total'] or 0
    visitantes_hoje = chamadas_de_hoje.aggregate(total=Sum('visitantes'))['total'] or 0
    
    # Lista de últimas turmas ativas (CONSULTA CORRIGIDA)
    ultimas_chamadas = Chamada.objects.order_by('-data', '-id').select_related('turma')[:5]

    context = {
        'total_turmas': total_turmas,
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'presentes_hoje': presentes_hoje,
        'oferta_hoje': oferta_hoje,
        'visitantes_hoje': visitantes_hoje,
        'ultimas_chamadas': ultimas_chamadas,
    }
    return render(request, 'core/admin_dashboard.html', context)