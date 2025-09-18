from django.core.management.base import BaseCommand
from mailings.models import Mailing
from mailings.services import send_mailing


class Command(BaseCommand):
    help = 'Отправляет все НЕЗАВЕРШЕННЫЕ рассылки (со статусом "Создана")'

    def handle(self, *args, **options):
        # Упрощенный запрос: берем все рассылки со статусом "Создана"
        mailings_to_send = Mailing.objects.filter(status=Mailing.STATUS_CREATED)

        count = mailings_to_send.count()
        self.stdout.write(f"Найдено рассылок для отправки: {count}")

        if not mailings_to_send.exists():
            self.stdout.write(self.style.SUCCESS('Нет рассылок для отправки.'))
            return

        # Проходим по каждой найденной рассылке и отправляем ее
        for mailing in mailings_to_send:
            self.stdout.write(f"--- Отправка рассылки ID {mailing.pk} ('{mailing.message.subject}')...")
            try:
                send_mailing(mailing)
                self.stdout.write(self.style.SUCCESS(f'Рассылка ID {mailing.pk} успешно отправлена.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при отправке рассылки ID {mailing.pk}: {e}'))

        self.stdout.write(self.style.SUCCESS('Все найденные рассылки обработаны.'))

# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from mailings.models import Mailing
# from mailings.services import send_mailing
#
#
# class Command(BaseCommand):
#     help = 'Отправляет активные рассылки, время которых подошло'
#
#     def handle(self, *args, **options):
#         # Получаем текущее время
#         now = timezone.now()
#         self.stdout.write(f"Текущее время: {now}")
#
#         # Выбираем все рассылки, которые активны и находятся в нужном временном диапазоне
#         # Статус должен быть "создана" или "запущена"
#         active_mailings = Mailing.objects.filter(
#             start_time__lte=now,  # Время старта уже прошло
#             end_time__gte=now,  # Время окончания еще не наступило
#             status__in=[Mailing.STATUS_CREATED, Mailing.STATUS_STARTED]
#         )
#
#         self.stdout.write(f"Найдено активных рассылок для отправки: {active_mailings.count()}")
#
#         if not active_mailings.exists():
#             self.stdout.write(self.style.SUCCESS('Нет рассылок для отправки в данный момент.'))
#             return
#
#         # Проходим по каждой активной рассылке и отправляем ее
#         for mailing in active_mailings:
#             self.stdout.write(f"--- Обработка рассылки ID {mailing.pk} ---")
#             try:
#                 # Вызываем нашу сервисную функцию
#                 send_mailing(mailing)
#                 self.stdout.write(self.style.SUCCESS(f'Рассылка ID {mailing.pk} обработана.'))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f'Ошибка при обработке рассылки ID {mailing.pk}: {e}'))
#
#         self.stdout.write(self.style.SUCCESS('Все активные рассылки обработаны.'))


