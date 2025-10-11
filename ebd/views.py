from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Turma, Chamada, Aluno, RegistroAlunoChamada
from .forms import AlunoForm
from datetime import date
from django.db.models import Sum, Case, When, IntegerField

def home_page(request):
    return render(request, 'ebd/home.html')

@login_required
def dashboard(request):
    # Se o usuário for admin/staff, redireciona para o painel de admin
    if request.user.is_staff:
        return redirect('core:admin_dashboard')
    
    # Se não, continua com o fluxo normal de professor
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
            
            return redirect('ebd:turma_dashboard', turma_id=turma.id)
        else:
            messages.error(request, 'Código de acesso incorreto.')
    
    context = {'turma': turma}
    return render(request, 'ebd/acesso_turma.html', context)

@login_required
def turma_dashboard(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        return redirect('ebd:acesso_turma', turma_id=turma_id)
    
    turma = get_object_or_404(Turma, id=turma_id)
    context = {'turma': turma}
    return render(request, 'ebd/turma_dashboard.html', context)

@login_required
def chamada(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        return redirect('ebd:acesso_turma', turma_id=turma_id)

    turma = get_object_or_404(Turma, id=turma_id)
    hoje = date.today()
    obj_chamada, _ = Chamada.objects.get_or_create(turma=turma, data=hoje)

    if request.method == 'POST':
        obj_chamada.oferta_do_dia = request.POST.get('oferta_do_dia', 0)
        obj_chamada.visitantes = request.POST.get('visitantes', 0)
        obj_chamada.save()
        
        for aluno in turma.alunos.all():
            presente = f'presente_{aluno.id}' in request.POST
            biblia = f'biblia_{aluno.id}' in request.POST
            revista = f'revista_{aluno.id}' in request.POST
            contribuiu = f'contribuiu_{aluno.id}' in request.POST
            visitante = f'visitante_{aluno.id}' in request.POST
            participacao = request.POST.get(f'participacao_{aluno.id}', 'NADA')

            RegistroAlunoChamada.objects.update_or_create(
                chamada=obj_chamada,
                aluno=aluno,
                defaults={
                    'presente': presente,
                    'trouxe_biblia': biblia,
                    'trouxe_revista': revista,
                    'contribuiu': contribuiu,
                    'levou_visitante': visitante,
                    'participacao': participacao,
                }
            )
        
        messages.success(request, 'Chamada salva com sucesso!')
        return redirect('ebd:chamada', turma_id=turma.id)

    alunos_data = []
    semestre_inicio = date(hoje.year, 1, 1) if hoje.month < 7 else date(hoje.year, 7, 1)

    for aluno in turma.alunos.all().order_by('nome_completo'):
        registro, _ = RegistroAlunoChamada.objects.get_or_create(chamada=obj_chamada, aluno=aluno)
        
        pontuacao_semestre = RegistroAlunoChamada.objects.filter(
            aluno=aluno, chamada__data__gte=semestre_inicio
        ).aggregate(
            total_pontos=Sum(Case(When(presente=True, then=15), default=0, output_field=IntegerField())) +
                Sum(Case(When(contribuiu=True, then=10), default=0, output_field=IntegerField())) +
                Sum(Case(
                    When(participacao='MUITO', then=10),
                    When(participacao='MEDIANO', then=5),
                    default=0,
                    output_field=IntegerField()
                )) +
                Sum(Case(When(trouxe_biblia=True, then=5), default=0, output_field=IntegerField())) +
                Sum(Case(When(trouxe_revista=True, then=5), default=0, output_field=IntegerField())) +
                Sum(Case(When(levou_visitante=True, then=20), default=0, output_field=IntegerField()))
        )['total_pontos'] or 0

        alunos_data.append({
            'aluno': aluno,
            'registro': registro,
            'pontuacao_semestre': pontuacao_semestre
        })

    context = {
        'turma': turma,
        'chamada_de_hoje': obj_chamada,
        'alunos_data': alunos_data,
        'opcoes_participacao': RegistroAlunoChamada.Participacao.choices,
    }
    return render(request, 'ebd/chamada.html', context)

@login_required
def gerenciar_alunos(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        return redirect('ebd:acesso_turma', turma_id=turma_id)

    turma = get_object_or_404(Turma, id=turma_id)
    alunos = turma.alunos.all().order_by('nome_completo')
    context = {'turma': turma, 'alunos': alunos}
    return render(request, 'ebd/gerenciar_alunos.html', context)

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
            return redirect('ebd:gerenciar_alunos', turma_id=turma_id)
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
            return redirect('ebd:gerenciar_alunos', turma_id=turma_id)
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
        return redirect('ebd:gerenciar_alunos', turma_id=turma_id)
        
    context = {'aluno': aluno, 'turma': turma}
    return render(request, 'ebd/aluno_confirm_delete.html', context)