# Generated by Django 4.2.20 on 2025-04-21 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='release_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
