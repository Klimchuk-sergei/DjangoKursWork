from django.urls import path
from .apps import MailingsConfig
from .views import (
    home, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageDeleteView, MessageUpdateView,MessageDetailView,
    MailingListView, MailingCreateView, MailingDeleteView, MailingDetailView, MailingUpdateView
)

app_name = 'mailings'

urlpatterns = [

    # Маршрут главной страницы
    path('', home, name='home'),

    # Маршруты для клиентов
    path('client/', ClientListView.as_view(), name='client-list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/create/', ClientCreateView.as_view(), name='client-create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),

    # Маршруты для сообщений
    path('message/', MessageListView.as_view(), name='message-list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),

    #Маршруты для рассылок
    path('mailing/', MailingListView.as_view(), name='mailing-list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing-update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing-delete'),
]