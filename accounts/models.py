from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return settings.STATIC_URL + "assets/img/profiles/avatar-01.jpg"

    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')],
        blank=True,
        null=True
    )
    is_online = models.BooleanField(default=False)
    show_friends_status = models.BooleanField(default=True)  # Do‘stlar statusi

    last_seen = models.DateTimeField(default=now)

    def update_last_seen(self):
        self.last_seen = now()
        self.save(update_fields=["last_seen"])

    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username