from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from datetime import datetime, timedelta
from .forms import FeedbackForm, LoginForm, AdminNoteForm, SatisfactionForm, InstitutionForm
from .models import Feedback, Institution
from django.http import JsonResponse

# Student-side: Feedback submission
def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            messages.success(request, 'Obrigado pelo seu feedback! Entraremos em contato em breve.')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'home.html', {'form': form})

# Student-side: Help page
def help_page(request):
    return render(request, 'help.html')

# Student-side: Satisfaction rating
def satisfaction_rating(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        form = SatisfactionForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Obrigado pela sua avaliação!')
            return redirect('home')
    else:
        form = SatisfactionForm(instance=feedback)
    return render(request, 'satisfaction.html', {'form': form, 'feedback': feedback})

# Admin-side: Login
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Admin-side: Logout
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Admin-side: Dashboard with educational metrics
@login_required
def dashboard(request):
    # Filtros
    filter_type = request.GET.get('type')
    filter_category = request.GET.get('category')
    filter_status = request.GET.get('status')
    filter_priority = request.GET.get('priority')
    selected_institution = request.GET.get('institution')
    
    feedbacks = Feedback.objects.all()
    
    # Filtrar por instituição se selecionada
    if selected_institution:
        # Verificar se o usuário tem autorização para acessar esta instituição
        if not request.user.is_superuser:
            authorized_institutions = Institution.objects.filter(
                is_active=True,
                authorized_users=request.user
            ).values_list('code', flat=True)
            
            if selected_institution not in authorized_institutions:
                messages.error(request, 'Você não tem autorização para acessar esta instituição.')
                return redirect('dashboard')
        
        feedbacks = feedbacks.filter(institution__code=selected_institution)
    
    # Aplicar filtros
    if filter_type in dict(Feedback.TYPE_CHOICES):
        feedbacks = feedbacks.filter(type=filter_type)
    if filter_category in dict(Feedback.CATEGORY_CHOICES):
        feedbacks = feedbacks.filter(category=filter_category)
    if filter_status in dict(Feedback.STATUS_CHOICES):
        feedbacks = feedbacks.filter(status=filter_status)
    if filter_priority in dict(Feedback.PRIORITY_CHOICES):
        feedbacks = feedbacks.filter(priority=filter_priority)
    
    # Estatísticas educacionais
    stats = {
        'total': Feedback.objects.count(),
        'pending': Feedback.objects.filter(status='pending').count(),
        'in_progress': Feedback.objects.filter(status='in_progress').count(),
        'resolved': Feedback.objects.filter(status='resolved').count(),
        'closed': Feedback.objects.filter(status='closed').count(),
        'high_priority': Feedback.objects.filter(priority='high').count(),
        'suggestions': Feedback.objects.filter(type='suggestion').count(),
        'technical': Feedback.objects.filter(type='technical').count(),
        'complaints': Feedback.objects.filter(type='complaint').count(),
        'praises': Feedback.objects.filter(type='praise').count(),
        'questions': Feedback.objects.filter(type='question').count(),
    }
    
    # Média de satisfação
    avg_satisfaction = Feedback.objects.filter(satisfaction_rating__isnull=False).aggregate(
        avg_rating=Avg('satisfaction_rating')
    )['avg_rating'] or 0
    
    # Lista de instituições para o dropdown (apenas as autorizadas para o usuário)
    if request.user.is_superuser:
        # Superusuário pode ver todas as instituições
        institutions = Institution.objects.filter(is_active=True)
    else:
        # Usuário normal só vê as instituições às quais está autorizado
        institutions = Institution.objects.filter(
            is_active=True,
            authorized_users=request.user
        )
    
    context = {
        'feedbacks': feedbacks,
        'stats': stats,
        'avg_satisfaction': round(avg_satisfaction, 1),
        'type_choices': Feedback.TYPE_CHOICES,
        'category_choices': Feedback.CATEGORY_CHOICES,
        'status_choices': Feedback.STATUS_CHOICES,
        'priority_choices': Feedback.PRIORITY_CHOICES,
        'institutions': institutions,
        'selected_institution': selected_institution,
    }
    
    return render(request, 'dashboard.html', context)

# Admin-side: Update status
@login_required
def update_status(request, pk, status):
    feedback = get_object_or_404(Feedback, pk=pk)
    if status in dict(Feedback.STATUS_CHOICES):
        feedback.status = status
        if status == 'resolved':
            feedback.date_resolved = datetime.now()
        feedback.save()
        messages.success(request, f'Status atualizado para {feedback.get_status_display()}.')
    
    # Manter o filtro de instituição
    institution = request.GET.get('institution')
    if institution:
        return redirect(f'{request.build_absolute_uri("dashboard")}?institution={institution}')
    return redirect('dashboard')

# Admin-side: Update priority
@login_required
def update_priority(request, pk, priority):
    feedback = get_object_or_404(Feedback, pk=pk)
    if priority in dict(Feedback.PRIORITY_CHOICES):
        feedback.priority = priority
        feedback.save()
        messages.success(request, f'Prioridade atualizada para {feedback.get_priority_display()}.')
    
    # Manter o filtro de instituição
    institution = request.GET.get('institution')
    if institution:
        return redirect(f'{request.build_absolute_uri("dashboard")}?institution={institution}')
    return redirect('dashboard')

# Admin-side: Prioritize all pending
@login_required
def prioritize_all(request):
    # Filtrar por instituição se especificada
    institution = request.GET.get('institution')
    pending_feedbacks = Feedback.objects.filter(status='pending')
    
    if institution:
        pending_feedbacks = pending_feedbacks.filter(institution__code=institution)
    
    count = pending_feedbacks.update(priority='high')
    messages.success(request, f'{count} feedbacks pendentes foram priorizados como alta prioridade.')
    
    # Manter o filtro de instituição
    if institution:
        return redirect(f'{request.build_absolute_uri("dashboard")}?institution={institution}')
    return redirect('dashboard')

# Admin-side: Assign feedback
@login_required
def assign_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        assigned_to = request.POST.get('assigned_to')
        if assigned_to:
            feedback.assigned_to = assigned_to
            feedback.status = Feedback.STATUS_IN_PROGRESS
            feedback.save()
            messages.success(request, f'Feedback atribuído para {assigned_to}.')
    return redirect('dashboard')

# Admin-side: Delete feedback
@login_required
def delete_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    messages.success(request, 'Registro excluído.')
    
    # Manter o filtro de instituição
    institution = request.GET.get('institution')
    if institution:
        return redirect(f'{request.build_absolute_uri("dashboard")}?institution={institution}')
    return redirect('dashboard')

# Admin-side: Add admin note
@login_required
def add_admin_note(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        form = AdminNoteForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota administrativa adicionada.')
    
    # Manter o filtro de instituição
    institution = request.GET.get('institution') or request.POST.get('institution')
    if institution:
        return redirect(f'{request.build_absolute_uri("dashboard")}?institution={institution}')
    return redirect('dashboard')

# Admin-side: Educational reports
@login_required
def reports(request):
    # Estatísticas por categoria
    category_stats = Feedback.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Estatísticas por tipo
    type_stats = Feedback.objects.values('type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Tempo médio de resolução
    resolved_feedbacks = Feedback.objects.filter(
        status=Feedback.STATUS_RESOLVED,
        date_resolved__isnull=False
    )
    
    avg_resolution_time = 0
    if resolved_feedbacks.exists():
        total_time = sum([
            (fb.date_resolved - fb.date_submitted).total_seconds() / 3600
            for fb in resolved_feedbacks
        ])
        avg_resolution_time = total_time / resolved_feedbacks.count()
    
    context = {
        'category_stats': category_stats,
        'type_stats': type_stats,
        'avg_resolution_time': round(avg_resolution_time, 1),
        'total_resolved': resolved_feedbacks.count(),
    }
    return render(request, 'reports.html', context)

@login_required
def create_institution(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid():
            institution = form.save()
            return JsonResponse({'success': True, 'name': institution.name, 'code': institution.code})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = InstitutionForm()
    return render(request, 'partials/institution_form.html', {'form': form})
