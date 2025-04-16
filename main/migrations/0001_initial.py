# Generated by Django 4.2.20 on 2025-04-14 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_description', models.CharField(max_length=1000)),
                ('tickets_no', models.IntegerField()),
                ('release_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.FloatField()),
            ],
        ),
    ]
