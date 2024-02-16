# Generated by Django 5.0.2 on 2024-02-15 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_user_all_point_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='point',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
