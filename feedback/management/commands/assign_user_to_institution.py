from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from feedback.models import Institution

class Command(BaseCommand):
    help = 'Associa um usuário a uma instituição'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome do usuário')
        parser.add_argument('institution_code', type=str, help='Código da instituição')

    def handle(self, *args, **options):
        username = options['username']
        institution_code = options['institution_code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuário "{username}" não encontrado.')
            )
            return

        try:
            institution = Institution.objects.get(code=institution_code)
        except Institution.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Instituição com código "{institution_code}" não encontrada.')
            )
            return

        # Adiciona o usuário à instituição
        institution.authorized_users.add(user)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Usuário "{username}" associado com sucesso à instituição "{institution.name}"!'
            )
        ) 