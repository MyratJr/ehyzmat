# Generated by Django 5.0.2 on 2024-02-10 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_delete_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regions',
            name='name',
            field=models.CharField(max_length=16),
        ),
    ]
