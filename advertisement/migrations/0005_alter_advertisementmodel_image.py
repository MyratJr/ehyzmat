# Generated by Django 5.0.2 on 2024-02-14 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_alter_advertisementmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementmodel',
            name='image',
            field=models.ImageField(max_length=255, upload_to='advertisements/%Y/%m/'),
        ),
    ]
