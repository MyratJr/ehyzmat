from django.db import models


class advertisementModel(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='advertisements/%Y/%m/', max_length=255)
    is_active = models.BooleanField(default=True)
    expired_date = models.DateField()

    def __str__(self):
        return self.title