from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingLog


def send_mailing(mailing: Mailing):
    """
    Сервисная функция для отправки рассылки.
    """
    print(f"Отправка рассылки: '{mailing.message.subject}'")

    try:
        # Получаем всех получателей из рассылки
        clients = mailing.clients.all()
        client_emails = [client.email for client in clients]

        # Отправляем письмо сразу всем получателям
        sent_count = send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=client_emails,
            fail_silently=False,  # Важно, чтобы видеть ошибки
        )

        # Если отправка прошла успешно (send_mail возвращает 1)
        if sent_count > 0:
            # Обновляем статус рассылки, если она была "Создана"
            if mailing.status == Mailing.STATUS_CREATED:
                mailing.status = Mailing.STATUS_STARTED
                mailing.save()

            # Создаем успешный лог для каждого получателя
            for client in clients:
                MailingLog.objects.create(
                    status=MailingLog.STATUS_SUCCESS,
                    server_response="Письмо успешно отправлено",
                    mailing=mailing,
                    client=client
                )
            print("Рассылка успешно отправлена.")

    except Exception as e:
        # Если произошла любая ошибка при отправке
        # Создаем лог с ошибкой для всех получателей (упрощенно)
        for client in mailing.clients.all():
            MailingLog.objects.create(
                status=MailingLog.STATUS_FAILED,
                server_response=str(e),
                mailing=mailing,
                client=client
            )
        print(f"Ошибка при отправке рассылки: {e}")
