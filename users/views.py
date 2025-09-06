from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User

class UserRegisterView(CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):

        #Сохраняем пользователя
        response = super().form_valid(form)
        user = form.save()

        #Отправляем письмо
        send_mail(
            subject='Поздравляем с регистрацией!',
            message='Вы успешно зарегистрировались в сервисе рассылок',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return response


class UserLoginView(LoginView):
    """Контролер для входа пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserProfileView(LoginRequiredMixin, UpdateView):
    """контролер для просмотра и редактирования профился."""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserLogoutView(LogoutView):
    """контролер выхода пользователя"""
    pass
