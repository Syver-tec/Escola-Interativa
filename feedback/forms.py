from django import forms
from .models import Feedback
from django.contrib.auth.forms import AuthenticationForm

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'name', 'email', 'type', 'category', 'message',
            'student_id', 'course', 'semester', 'teacher', 'subject'
        ]
        exclude = ['institution']  # Campo será preenchido automaticamente
        widgets = {
            'type': forms.Select(choices=Feedback.TYPE_CHOICES),
            'category': forms.Select(choices=Feedback.CATEGORY_CHOICES),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva detalhadamente sua solicitação...'}),
            'student_id': forms.TextInput(attrs={'placeholder': 'Número da matrícula (opcional)'}),
            'course': forms.TextInput(attrs={'placeholder': 'Ex: Engenharia de Software'}),
            'semester': forms.TextInput(attrs={'placeholder': 'Ex: 2024.1'}),
            'teacher': forms.TextInput(attrs={'placeholder': 'Nome do professor (se aplicável)'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Nome da disciplina (se aplicável)'}),
        }
        labels = {
            'name': 'Nome Completo',
            'email': 'E-mail',
            'type': 'Tipo de Solicitação',
            'category': 'Categoria',
            'message': 'Mensagem',
            'student_id': 'Matrícula',
            'course': 'Curso',
            'semester': 'Semestre',
            'teacher': 'Professor',
            'subject': 'Disciplina',
        }

class AdminNoteForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['admin_note', 'assigned_to', 'follow_up_needed']
        widgets = {
            'admin_note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adicionar nota interna...'}),
            'assigned_to': forms.TextInput(attrs={'placeholder': 'Responsável pela resolução'}),
        }
        labels = {
            'admin_note': 'Nota Administrativa',
            'assigned_to': 'Responsável',
            'follow_up_needed': 'Necessita Acompanhamento',
        }

class SatisfactionForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['satisfaction_rating']
        widgets = {
            'satisfaction_rating': forms.Select(choices=[
                (1, '1 - Muito Insatisfeito'),
                (2, '2 - Insatisfeito'),
                (3, '3 - Neutro'),
                (4, '4 - Satisfeito'),
                (5, '5 - Muito Satisfeito'),
            ])
        }
        labels = {
            'satisfaction_rating': 'Como você avalia o atendimento?',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={'autofocus': True})) 