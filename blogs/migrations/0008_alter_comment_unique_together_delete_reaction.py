# Generated by Django 4.2.3 on 2023-10-09 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_author_id'),
        ('blogs', '0007_alter_reaction_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('owner', 'blog')},
        ),
        migrations.DeleteModel(
            name='Reaction',
        ),
    ]
