from django.db import models
from django.contrib.auth.models import AbstractUser
from advertisement.views import validate_image, phone_regex


class User(AbstractUser):
    avatar = models.ImageField(upload_to="user/avatar_images", default="user/avatar_images/8380015.jpg")
    banner_image = models.ImageField(upload_to="user/avatar_bg_images", validators=[validate_image], default="user/avatar_bg_images/18220884_v1016-b-09.jpg")
    experience = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    web = models.URLField(max_length=200, blank=True, null=True)
    tiktok = models.CharField(max_length=50, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    imo = models.CharField(max_length=50, blank=True, null=True)
    fisrt_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=12)
    rate_point = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    rate_point_total = models.IntegerField(default=0)
    point_counter = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)
    like_counter = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)