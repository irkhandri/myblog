# Generated by Django 4.2.3 on 2023-10-10 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_message_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='owner',
            new_name='sender',
        ),
    ]
