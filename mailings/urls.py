from django.urls import path
from .apps import MailingsConfig
from .views import (
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageDeleteView, MessageUpdateView,MessageDetailView,
    MailingListView, MailingCreateView, MailingDeleteView, MailingDetailView, MailingUpdateView
)

app_name = MailingsConfig.name

urlpatterns = [
    # Маршруты для клиентов
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),

    # Маршруты для сообщений
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),

    #Маршруты для рассылок
    path('mailing/', MailingListView.as_view(), name='mailing-list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing-update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing-delete'),
]