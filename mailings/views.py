from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Client, Message, Mailing, MailingLog
from .forms import ClientForm, MessageForm, MailingForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from services import send_mailing


class OwnerRequiredMixin(AccessMixin):
    """Миксин для проверки прав пользователя как владельца"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user

        # Проверяем, явлется ли пользователь владельцем
        if user.is_staff or user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return super().dispatch(request, *args, **kwargs)

        if obj.owner == user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("У вас нет прав для доступа к этому обьекту")


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff or user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return queryset

        return super().get_queryset().filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, OwnerRequiredMixin,  DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.has_perm('auth.delete_client')


# CRUD сообщенией

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff or user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return queryset

        return super().get_queryset().filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


# CRUD рассылок

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    def get_queryset(self):
        queryset = super().get_queyset()
        user = self.request.user

        if user.is_staff or user.is_superuser or user.groups.filter(name='Менеджеры').exists():
            return queryset

        return super().get_queryset().filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')

def home(request):
    """Контролер главной страницы, показывает статистику рассылок"""
    if request.user.is_authenticated:
        all_mailings = Mailing.objects.filter(owner=request.user)
        active_mailings_count = all_mailings.filter(status='started').count()
        clients_count = Client.objects.filter(owner=request.user).distinct().count()
    else:
        all_mailings = Mailing.objects.none()
        active_mailings_count = 0
        clients_count = 0

    context = {
        'all_mailings_count': all_mailings.count(),
        'active_mailings_count': active_mailings_count,
        'clients_count': clients_count,
        'title': 'Главная страница'
    }

    return render(request, 'mailings/home.html', context)


class MailingSendView(LoginRequiredMixin, View):
    """
    Контроллер для ручной отправки рассылки.
    """

    def get(self, request, pk):
        # Получаем объект рассылки или возвращаем 404
        mailing = get_object_or_404(Mailing, pk=pk)

        # Проверяем, что текущий пользователь является владельцем
        if mailing.owner == request.user:
            # Вызываем нашу сервисную функцию
            send_mailing(mailing)

        # Перенаправляем пользователя обратно на детальную страницу рассылки
        return redirect('mailings:mailing_detail', pk=pk)


class MailingLogListView(LoginRequiredMixin, ListView):
    """
    Контроллер для просмотра логов по рассылке.
    """
    model = MailingLog
    template_name = 'mailings/mailing_logs.html'
    context_object_name = 'logs'

    def get_queryset(self):
        """
        Фильтруем логи, чтобы показать только те, которые относятся
        к рассылке с pk из URL и принадлежат текущему пользователю.
        """

        queryset = super().get_queryset().filter(mailing__owner=self.request.user)
        mailing_pk = self.kwargs.get('pk')
        return queryset.filter(mailing__pk=mailing_pk)

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст саму рассылку для вывода заголовка.
        """
        context = super().get_context_data(**kwargs)
        mailing_pk = self.kwargs.get('pk')
        context['mailing'] = get_object_or_404(Mailing, pk=mailing_pk)
        context['title'] = f"Отчет по рассылке: {context['mailing'].message.subject}"
        return context