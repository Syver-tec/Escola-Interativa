from django.core.management.base import BaseCommand
from feedback.models import Institution

class Command(BaseCommand):
    help = 'Cria uma nova instituição educacional'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Nome da instituição')
        parser.add_argument('code', type=str, help='Código único da instituição')
        parser.add_argument('--email', type=str, help='Email de contato')
        parser.add_argument('--phone', type=str, help='Telefone')
        parser.add_argument('--address', type=str, help='Endereço')

    def handle(self, *args, **options):
        name = options['name']
        code = options['code']
        email = options.get('email', '')
        phone = options.get('phone', '')
        address = options.get('address', '')

        # Verifica se já existe uma instituição com este código
        if Institution.objects.filter(code=code).exists():
            self.stdout.write(
                self.style.ERROR(f'Erro: Já existe uma instituição com o código "{code}"')
            )
            return

        # Cria a instituição
        institution = Institution.objects.create(
            name=name,
            code=code,
            email=email,
            phone=phone,
            address=address
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Instituição "{name}" criada com sucesso!\n'
                f'Código: {code}\n'
                f'URL do Admin: http://localhost:8000/{code}/admin/dashboard/\n'
                f'URL do Formulário: http://localhost:8000/{code}/'
            )
        ) 