from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


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

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        # формируем ссылку для пользователя, обязательно передавая данные в kwargs
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        # формируем полный адрес(не забыть прописать DOMAIN_NAME в settings
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдтите по ссылке {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='ddd@example.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )
    # Проверка просрочена ли ссылка или нет
    def is_expired(self):
        return True if now() >= self.expiration else False
