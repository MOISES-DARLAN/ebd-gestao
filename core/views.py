from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from ebd.models import Turma, Aluno, Chamada, RegistroAlunoChamada
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum, Count, Case, When, IntegerField, Avg, F

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
def admin_dashboard(request):
    hoje = date.today()
    semestre_inicio = date(hoje.year, 1, 1) if hoje.month < 7 else date(hoje.year, 7, 1)

    total_turmas = Turma.objects.count()
    total_alunos = Aluno.objects.count()
    total_professores = User.objects.filter(is_staff=False).count()

    chamadas_de_hoje = Chamada.objects.filter(data=hoje)
    presentes_hoje = RegistroAlunoChamada.objects.filter(chamada__in=chamadas_de_hoje, presente=True).count()
    oferta_hoje = chamadas_de_hoje.aggregate(total=Sum('oferta_do_dia'))['total'] or 0
    visitantes_hoje = chamadas_de_hoje.aggregate(total=Sum('visitantes'))['total'] or 0
    
    ultimas_chamadas = Chamada.objects.order_by('-data', '-id').select_related('turma')[:5]

    turmas = Turma.objects.filter(alunos__isnull=False).distinct()
    ranking_diario = []
    ranking_semestral = []

    pontuacao = Sum(Case(When(presente=True, then=15), default=0)) + \
                Sum(Case(When(contribuiu=True, then=10), default=0)) + \
                Sum(Case(When(participacao='MUITO', then=10), When(participacao='MEDIANO', then=5), default=0)) + \
                Sum(Case(When(trouxe_biblia=True, then=5), default=0)) + \
                Sum(Case(When(trouxe_revista=True, then=5), default=0)) + \
                Sum(Case(When(levou_visitante=True, then=20), default=0))

    for turma in turmas:
        num_alunos = turma.alunos.count()
        if num_alunos > 0:
            pontos_hoje = RegistroAlunoChamada.objects.filter(
                chamada__turma=turma, chamada__data=hoje
            ).aggregate(total=pontuacao)['total'] or 0
            ranking_diario.append({'turma': turma, 'media': pontos_hoje / num_alunos})

            pontos_semestre = RegistroAlunoChamada.objects.filter(
                chamada__turma=turma, chamada__data__gte=semestre_inicio
            ).aggregate(total=pontuacao)['total'] or 0
            ranking_semestral.append({'turma': turma, 'media': pontos_semestre / num_alunos})

    ranking_diario.sort(key=lambda x: x['media'], reverse=True)
    ranking_semestral.sort(key=lambda x: x['media'], reverse=True)

    context = {
        'hoje': hoje,
        'total_turmas': total_turmas,
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'presentes_hoje': presentes_hoje,
        'oferta_hoje': oferta_hoje,
        'visitantes_hoje': visitantes_hoje,
        'ultimas_chamadas': ultimas_chamadas,
        'ranking_diario': ranking_diario,
        'ranking_semestral': ranking_semestral,
    }
    return render(request, 'core/admin_dashboard.html', context)