# Generated by Django 5.0.2 on 2024-03-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='title',
            field=models.CharField(default='Default Title', max_length=50),
        ),
    ]
