# Generated by Django 5.0.2 on 2024-02-14 08:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0009_alter_service_category_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.services')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorited_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited-user+', to=settings.AUTH_USER_MODEL)),
                ('favoriting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoriting-user+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Viewed_Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.services')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Viewing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed-user+', to=settings.AUTH_USER_MODEL)),
                ('viewing_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewing-user+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
