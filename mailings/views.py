from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Client, Message, Mailing
from .forms import ClientForm, MessageForm, MailingForm
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(AccessMixin):
    """Миксин для проверки прав пользователя как владельца"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # Проверяем, явлется ли пользователь владельцем
        if obj.owner != request.user:
            raise PermissionDenied("У вас нет прав доступа.")

        return super().dispatch(request, *args, **kwargs)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
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


class ClientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


# CRUD сообщенией

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    def get_queryset(self):
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


class MessageUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


# CRUD рассылок

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    def get_queryset(self):
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


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
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
