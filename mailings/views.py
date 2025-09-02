from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Client, Message, Mailing
from .forms import ClientForm, MessageForm, MailingForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OwnerMixin:
    """Миксин для проверки прав пользователя как владельца"""
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

class ClientListView(LoginRequiredMixin, ListView):
    model = Client

class ClientDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Client

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client-list')

class ClientDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client-list')

class MessageListView(LoginRequiredMixin, OwnerMixin, ListView):
    model = Message

class MessageDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Message

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message-list')

class MessageDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message-list')

# <--CRUD рассылок-->

class MailingListView(LoginRequiredMixin, OwnerMixin, ListView):
    model = Mailing

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Mailing

class MailingUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing-list')

class MailingDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing-list')

