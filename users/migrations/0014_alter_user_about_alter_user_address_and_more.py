# Generated by Django 5.0.2 on 2024-02-13 18:15

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_user_about_alter_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user/avatar_images/8380015.jpg', upload_to='user/avatar_images'),
        ),
        migrations.AlterField(
            model_name='user',
            name='banner_image',
            field=models.ImageField(default='user/avatar_bg_images/18220884_v1016-b-09.jpg', upload_to='user/avatar_bg_images', validators=[users.models.validate_image]),
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='imo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='instagram',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tiktok',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='webpage',
            field=models.URLField(blank=True, null=True),
        ),
    ]
