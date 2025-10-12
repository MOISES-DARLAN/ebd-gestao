from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Turma, Chamada, Aluno
from datetime import date

def home_page(request):
    return render(request, 'ebd/home.html')

@login_required
def dashboard(request):
    turmas = Turma.objects.all().order_by('nome')
    context = {'turmas': turmas}
    return render(request, 'ebd/dashboard.html', context)

@login_required
def acesso_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        codigo = request.POST.get('codigo_acesso')
        if codigo == turma.codigo_acesso:
            # Inicializa a lista de turmas autorizadas na sessão se não existir
            if 'turmas_autorizadas' not in request.session:
                request.session['turmas_autorizadas'] = []
            
            # Adiciona o ID da turma à lista na sessão
            if turma_id not in request.session['turmas_autorizadas']:
                request.session['turmas_autorizadas'].append(turma_id)
                request.session.save() # Salva a sessão explicitamente
            
            return redirect('chamada', turma_id=turma.id)
        else:
            messages.error(request, 'Código de acesso incorreto.')
    
    context = {'turma': turma}
    return render(request, 'ebd/acesso_turma.html', context)


@login_required
def chamada(request, turma_id):
    # Verifica se o professor tem permissão para esta turma na sessão
    if turma_id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado. Por favor, insira o código da turma.')
        return redirect('acesso_turma', turma_id=turma_id)

    turma = get_object_or_404(Turma, id=turma_id)
    hoje = date.today()

    if request.method == 'POST':
        ids_alunos_presentes = request.POST.getlist('presentes')
        obj_chamada, created = Chamada.objects.get_or_create(turma=turma, data=hoje)
        
        obj_chamada.alunos_presentes.clear()
        
        for aluno_id in ids_alunos_presentes:
            aluno = Aluno.objects.get(id=aluno_id)
            obj_chamada.alunos_presentes.add(aluno)
        
        messages.success(request, 'Chamada salva com sucesso!')
        return redirect('chamada', turma_id=turma.id)

    alunos_da_turma = turma.alunos.all().order_by('nome_completo')
    chamada_de_hoje = Chamada.objects.filter(turma=turma, data=hoje).first()
    ids_presentes_hoje = []
    if chamada_de_hoje:
        ids_presentes_hoje = chamada_de_hoje.alunos_presentes.values_list('id', flat=True)

    context = {
        'turma': turma,
        'alunos': alunos_da_turma,
        'ids_presentes_hoje': ids_presentes_hoje
    }
    return render(request, 'ebd/chamada.html', context)