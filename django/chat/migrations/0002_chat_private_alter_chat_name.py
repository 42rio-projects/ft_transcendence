# Generated by Django 5.0.2 on 2024-02-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='name',
            field=models.CharField(max_length=301, unique=True),
        ),
    ]
