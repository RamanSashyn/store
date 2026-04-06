from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    # Также надо добавить поле которое будет отвечать за подтверждение почты пользователем


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    # Поле для генерации уникальной ссылки для конкретного пользователя после регистрации
    # UUIDField поле которое формирует универсальный уникальный аутификатор
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    # Когда заканчивается срок действия ссылки

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
