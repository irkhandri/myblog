# Generated by Django 4.2.5 on 2023-10-02 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('vote_total', models.IntegerField(blank=True, default=0, null=True)),
                ('vote_like', models.IntegerField(blank=True, default=0, null=True)),
                ('vote_unlike', models.IntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('comment', models.CharField(choices=[('like', 'Like '), ('unlike', 'Unlike')], max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
