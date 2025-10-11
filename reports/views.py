from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ebd.models import Turma, Chamada, RegistroAlunoChamada, Aluno
from django.db.models import Count, Q, Sum, Case, When, IntegerField
from datetime import date
import json

@login_required
def attendance_history(request, turma_id):
    if not request.user.is_staff and turma_id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado.')
        return redirect('ebd:acesso_turma', turma_id=turma_id)

    turma = get_object_or_404(Turma, id=turma_id)
    
    historico = Chamada.objects.filter(turma=turma).order_by('-data').annotate(
        presentes_count=Count('registroalunochamada', filter=Q(registroalunochamada__presente=True))
    )
    
    context = { 'turma': turma, 'historico': historico }
    return render(request, 'reports/attendance_history.html', context)

@login_required
def chamada_detalhes(request, chamada_id):
    chamada = get_object_or_404(Chamada, id=chamada_id)

    if not request.user.is_staff and chamada.turma.id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado.')
        return redirect('ebd:dashboard')

    registros = RegistroAlunoChamada.objects.filter(chamada=chamada).select_related('aluno').order_by('aluno__nome_completo')
    
    context = { 'chamada': chamada, 'registros': registros }
    return render(request, 'reports/chamada_detalhes.html', context)

@login_required
def analise_turma(request, turma_id):
    if not request.user.is_staff and turma_id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado.')
        return redirect('ebd:acesso_turma', turma_id=turma_id)
    
    turma = get_object_or_404(Turma, id=turma_id)
    hoje = date.today()
    semestre_inicio = date(hoje.year, 1, 1) if hoje.month < 7 else date(hoje.year, 7, 1)

    pontuacao_alunos = Aluno.objects.filter(turma=turma).annotate(
        total_pontos=Sum(
            Case(When(registroalunochamada__presente=True, then=15), default=0, output_field=IntegerField()),
            filter=Q(registroalunochamada__chamada__data__gte=semestre_inicio)
        ) +
        Sum(
            Case(When(registroalunochamada__contribuiu=True, then=10), default=0, output_field=IntegerField()),
            filter=Q(registroalunochamada__chamada__data__gte=semestre_inicio)
        ) +
        Sum(
            Case(
                When(registroalunochamada__participacao='MUITO', then=10),
                When(registroalunochamada__participacao='MEDIANO', then=5),
                default=0, output_field=IntegerField()
            ),
            filter=Q(registroalunochamada__chamada__data__gte=semestre_inicio)
        ) +
        Sum(
            Case(When(registroalunochamada__trouxe_biblia=True, then=5), default=0, output_field=IntegerField()),
            filter=Q(registroalunochamada__chamada__data__gte=semestre_inicio)
        ) +
        Sum(
            Case(When(registroalunochamada__trouxe_revista=True, then=5), default=0, output_field=IntegerField()),
            filter=Q(registroalunochamada__chamada__data__gte=semestre_inicio)
        ) +
        Sum(
            Case(When(registroalunochamada__levou_visitante=True, then=20), default=0, output_field=IntegerField()),
            filter=Q(registroalunochamada__chamada__data__gte=semestre_inicio)
        )
    ).order_by('-total_pontos')[:10]

    ranking_labels = [aluno.nome_completo for aluno in pontuacao_alunos]
    ranking_data = [aluno.total_pontos for aluno in pontuacao_alunos]

    frequencia = Chamada.objects.filter(
        turma=turma, data__gte=semestre_inicio
    ).annotate(
        presentes_count=Count('registroalunochamada', filter=Q(registroalunochamada__presente=True))
    ).order_by('data')

    frequencia_labels = [chamada.data.strftime('%d/%m') for chamada in frequencia]
    frequencia_data = [chamada.presentes_count for chamada in frequencia]

    context = {
        'turma': turma,
        'ranking_labels': json.dumps(ranking_labels),
        'ranking_data': json.dumps(ranking_data),
        'frequencia_labels': json.dumps(frequencia_labels),
        'frequencia_data': json.dumps(frequencia_data),
    }
    return render(request, 'reports/analise_turma.html', context)