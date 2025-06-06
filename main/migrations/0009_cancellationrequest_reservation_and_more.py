# Generated by Django 4.2.20 on 2025-04-19 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_remove_cancellationrequest_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancellationrequest',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.ticketspurchased'),
        ),
        migrations.AddField(
            model_name='cancellationrequest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
