# Generated by Django 5.0.2 on 2024-02-15 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_user_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='point',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
    ]
