# Generated by Django 5.0.4 on 2024-06-05 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_provider_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='address',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
