# Generated by Django 5.0.2 on 2024-02-16 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_rename_district_region_districts_region'),
    ]

    operations = [
        migrations.RenameField(
            model_name='districts',
            old_name='name',
            new_name='district',
        ),
    ]
