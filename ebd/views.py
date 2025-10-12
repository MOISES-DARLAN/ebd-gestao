from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Turma, Chamada, Aluno
from .forms import AlunoForm
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
            if 'turmas_autorizadas' not in request.session:
                request.session['turmas_autorizadas'] = []
            
            if turma_id not in request.session['turmas_autorizadas']:
                request.session['turmas_autorizadas'].append(turma_id)
                request.session.modified = True
            
            return redirect('ebd:chamada', turma_id=turma.id)
        else:
            messages.error(request, 'Código de acesso incorreto.')
    
    context = {'turma': turma}
    return render(request, 'ebd/acesso_turma.html', context)


@login_required
def chamada(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado. Por favor, insira o código da turma.')
        return redirect('ebd:acesso_turma', turma_id=turma_id)

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
        return redirect('ebd:chamada', turma_id=turma.id)

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

@login_required
def aluno_create(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        return redirect('ebd:acesso_turma', turma_id=turma_id)
    
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save()
            turma.alunos.add(aluno)
            messages.success(request, f"Aluno '{aluno.nome_completo}' cadastrado com sucesso!")
            return redirect('ebd:chamada', turma_id=turma_id)
    else:
        form = AlunoForm()
        
    context = {'form': form, 'turma': turma, 'titulo': 'Adicionar Novo Aluno'}
    return render(request, 'ebd/aluno_form.html', context)

@login_required
def aluno_update(request, turma_id, aluno_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        return redirect('ebd:acesso_turma', turma_id=turma_id)
    
    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, f"Dados do aluno '{aluno.nome_completo}' atualizados com sucesso!")
            return redirect('ebd:chamada', turma_id=turma_id)
    else:
        form = AlunoForm(instance=aluno)
        
    context = {'form': form, 'turma': turma, 'titulo': 'Editar Aluno'}
    return render(request, 'ebd/aluno_form.html', context)

@login_required
def aluno_delete(request, turma_id, aluno_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        return redirect('ebd:acesso_turma', turma_id=turma_id)
        
    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    if request.method == 'POST':
        nome_aluno = aluno.nome_completo
        turma.alunos.remove(aluno)
        aluno.delete()
        messages.success(request, f"Aluno '{nome_aluno}' excluído com sucesso.")
        return redirect('ebd:chamada', turma_id=turma_id)
        
    context = {'aluno': aluno, 'turma': turma}
    return render(request, 'ebd/aluno_confirm_delete.html', context)