# Generated by Django 4.2.3 on 2023-10-10 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_owner_message_sender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['is_read']},
        ),
    ]
