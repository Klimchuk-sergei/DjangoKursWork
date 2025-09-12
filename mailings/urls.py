from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .views import (
    home, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageDeleteView, MessageUpdateView, MessageDetailView,
    MailingListView, MailingCreateView, MailingDeleteView, MailingDetailView, MailingUpdateView,
    MailingSendView, MailingLogListView
)

app_name = 'mailings'

urlpatterns = [

    # Маршрут главной страницы
    path('', vary_on_cookie(cache_page(900)(home)), name='home'),

    # Маршруты для клиентов
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    # Маршруты для сообщений
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),

    # Маршруты для рассылок
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),
    path('mailings/<int:pk>/logs/', MailingLogListView.as_view(), name='mailing_logs'),
]
