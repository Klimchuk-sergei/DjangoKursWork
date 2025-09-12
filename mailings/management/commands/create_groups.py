from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Mailing, Client, Message
from users.models import User


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" с необходимыми правами'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        manager_group, created = Group.objects.get_or_create(name='Менеджеры')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" успешно создана.'))

        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        user_content_type = ContentType.objects.get_for_model(User)
        client_content_type = ContentType.objects.get_for_model(Client)
        message_content_type = ContentType.objects.get_for_model(Message)

        # Получаем права, которые мы определили в Meta
        can_disable_mailing = Permission.objects.get(
            codename='can_disable_mailing',
            content_type=mailing_content_type,
        )
        can_block_user = Permission.objects.get(
            codename='can_block_user',
            content_type=user_content_type,
        )

        view_mailing = Permission.objects.get(codename='view_mailing', content_type=mailing_content_type)
        view_user = Permission.objects.get(codename='view_user', content_type=user_content_type)
        view_client = Permission.objects.get(codename='view_client', content_type=client_content_type)
        view_message = Permission.objects.get(codename='view_message', content_type=message_content_type)

        # Добавляем все нужные права в группу
        manager_group.permissions.add(
            # Кастомные права
            can_disable_mailing,
            can_block_user,
            # Права на просмотр
            view_mailing,
            view_user,
            view_client,
            view_message
        )

        self.stdout.write(self.style.SUCCESS('Права успешно добавлены в группу "Менеджеры".'))
