from django.db import models
from django.conf import settings


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='email')
    full_name = models.CharField(max_length=250, verbose_name='Ф.И.О')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    """Тот кто добавил клиента"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='Владелец', null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    """Модель сообщения для рассылки"""
    subject = models.CharField(max_length=250, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    """Создатель письма"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец',
                              null=True, blank=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    # Статусы рассылки
    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена')
    ]
    FREQ_DAILY = 'daily'
    FREQ_WEEKLY = 'weekly'
    FREQ_MONTHLY = 'monthly'
    FREQ_CHOICES = [
        (FREQ_DAILY, 'Раз в день'),
        (FREQ_WEEKLY, 'Раз в неделю'),
        (FREQ_MONTHLY, 'Раз в месяц')
    ]
    # Время создания рассылки
    created_at = models.DateTimeField(auto_now_add=True)

    # Время начала рассылки
    start_time = models.DateTimeField(verbose_name='Время начала рассылки')

    # Время окончания рассылки
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')

    # Периодиность рассылки
    frequency = models.CharField(max_length=10,
                                 choices=FREQ_CHOICES,
                                 verbose_name='Периодичность',
                                 help_text='Выберите периодичность отправки сообщений'
                                 )

    # Выбор статуса рассылки из предопределеных значений
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=STATUS_CREATED,
                              verbose_name='Статус'
                              )

    message = models.ForeignKey('Message',
                                on_delete=models.CASCADE,
                                verbose_name='Сообщение'
                                )

    clients = models.ManyToManyField('Client', verbose_name='Клиенты'
                                     )

    # Владелец, который создал эту рассылку
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец',
                              null=True, blank=True
                              )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка '{self.message.subject}' в {self.start_time}"


class MailingLog(models.Model):
    """модель логов рассылки"""
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Не успешно')
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', null=True, blank=True)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'

    def __str__(self):
        return f"Попытка для '{self.mailing}' в {self.attempt_time} ({self.status})"
