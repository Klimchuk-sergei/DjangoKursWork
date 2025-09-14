from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомизация отображения модели User в админ-панели.
    """
    # Поля, которые будут отображаться
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)

    # Поля, по которым можно будет искать пользователей
    search_fields = ('email', 'first_name', 'last_name',)

    # Поля, по которым можно будет фильтровать список
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)


    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        # Секция с вашими кастомными полями
        ("Custom fields", {"fields": ("avatar", "phone_number", "country")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Поля, которые будут запрашиваться при создании нового пользователя в админке
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "password2"),
        }),
    )

    # Поле, по которому будет сортироваться список по умолчанию
    ordering = ('email',)
