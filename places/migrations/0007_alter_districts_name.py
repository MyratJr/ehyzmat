# Generated by Django 5.0.2 on 2024-02-10 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_districts_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='districts',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
