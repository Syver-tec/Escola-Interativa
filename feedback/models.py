from django.db import models

# Create your models here.

class Institution(models.Model):
    """Modelo para gerenciar múltiplas instituições educacionais"""
    name = models.CharField(max_length=200, verbose_name='Nome da Instituição')
    code = models.CharField(max_length=50, unique=True, verbose_name='Código Único')
    domain = models.CharField(max_length=100, blank=True, verbose_name='Domínio')
    address = models.TextField(blank=True, null=True, verbose_name='Endereço')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='Email de Contato')
    logo = models.ImageField(upload_to='institutions/logos/', blank=True, verbose_name='Logo')
    is_active = models.BooleanField(default=True, verbose_name='Ativa')
    # Usuários autorizados para esta instituição
    authorized_users = models.ManyToManyField('auth.User', blank=True, verbose_name='Usuários Autorizados')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    
    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_admin_url(self):
        """Retorna a URL do admin para esta instituição"""
        return f"/{self.code}/admin/dashboard/"

class Feedback(models.Model):
    # Tipos específicos para educação
    SUGGESTION = 'Suggestion'
    TECHNICAL = 'Technical'
    COMPLAINT = 'Complaint'
    PRAISE = 'Praise'
    DOUBT = 'Doubt'
    
    TYPE_CHOICES = [
        (SUGGESTION, 'Sugestão'),
        (TECHNICAL, 'Suporte Técnico'),
        (COMPLAINT, 'Reclamação'),
        (PRAISE, 'Elogio'),
        (DOUBT, 'Dúvida'),
    ]
    
    # Status educacional
    STATUS_PENDING = 'Pending'
    STATUS_IN_PROGRESS = 'In_Progress'
    STATUS_RESOLVED = 'Resolved'
    STATUS_CLOSED = 'Closed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendente'),
        (STATUS_IN_PROGRESS, 'Em Andamento'),
        (STATUS_RESOLVED, 'Resolvido'),
        (STATUS_CLOSED, 'Fechado'),
    ]
    
    # Prioridades educacionais
    PRIORITY_LOW = 'Low'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_HIGH = 'High'
    PRIORITY_URGENT = 'Urgent'
    
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Baixa'),
        (PRIORITY_MEDIUM, 'Média'),
        (PRIORITY_HIGH, 'Alta'),
        (PRIORITY_URGENT, 'Urgente'),
    ]
    
    # Categorias educacionais
    CATEGORY_ADMINISTRATIVE = 'Administrative'
    CATEGORY_ACADEMIC = 'Academic'
    CATEGORY_TECHNICAL = 'Technical'
    CATEGORY_FACILITY = 'Facility'
    CATEGORY_OTHER = 'Other'
    
    CATEGORY_CHOICES = [
        (CATEGORY_ADMINISTRATIVE, 'Administrativo'),
        (CATEGORY_ACADEMIC, 'Acadêmico'),
        (CATEGORY_TECHNICAL, 'Técnico'),
        (CATEGORY_FACILITY, 'Infraestrutura'),
        (CATEGORY_OTHER, 'Outro'),
    ]

    # Relacionamento com instituição
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instituição', null=True, blank=True)
    
    # Campos básicos
    name = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='E-mail')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Tipo')
    message = models.TextField(verbose_name='Mensagem')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='Status')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM, verbose_name='Prioridade')
    
    # Campos específicos da educação
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER, verbose_name='Categoria')
    student_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='Matrícula')
    course = models.CharField(max_length=100, blank=True, null=True, verbose_name='Curso')
    semester = models.CharField(max_length=20, blank=True, null=True, verbose_name='Semestre')
    teacher = models.CharField(max_length=100, blank=True, null=True, verbose_name='Professor')
    subject = models.CharField(max_length=100, blank=True, null=True, verbose_name='Disciplina')
    
    # Campos de rastreamento
    date_submitted = models.DateTimeField(auto_now_add=True, verbose_name='Data de Envio')
    date_resolved = models.DateTimeField(blank=True, null=True, verbose_name='Data de Resolução')
    admin_note = models.TextField(blank=True, null=True, verbose_name='Nota do Administrador')
    assigned_to = models.CharField(max_length=100, blank=True, null=True, verbose_name='Responsável')
    
    # Campos de feedback
    satisfaction_rating = models.IntegerField(blank=True, null=True, verbose_name='Avaliação de Satisfação')
    follow_up_needed = models.BooleanField(default=False, verbose_name='Necessita Acompanhamento')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.get_status_display()}"

    class Meta:
        ordering = ['-priority', '-date_submitted']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        
    def get_display_name(self):
        """Retorna nome de exibição com informações educacionais"""
        if self.student_id:
            return f"{self.name} (Matrícula: {self.student_id})"
        return self.name
    
    def is_urgent(self):
        """Verifica se é urgente baseado na prioridade e tempo"""
        from datetime import datetime, timedelta
        if self.priority == self.PRIORITY_URGENT:
            return True
        # Se passou mais de 48h e ainda está pendente
        if self.status == self.STATUS_PENDING:
            time_diff = datetime.now() - self.date_submitted.replace(tzinfo=None)
            return time_diff > timedelta(hours=48)
        return False
