# Generated by Django 4.2.5 on 2023-10-03 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('blogs', '0004_blog_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blogs.blog'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.author'),
        ),
    ]
