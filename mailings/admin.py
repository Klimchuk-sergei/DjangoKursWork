from django.contrib import admin
from .models import Client, Message, Mailing, MailingLog

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'owner',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'status', 'start_time', 'end_time', 'owner',)
    list_filter = ('status',)

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'client', 'attempt_time', 'status',)
    list_filter = ('status',)