# Generated by Django 4.2.5 on 2024-01-11 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_file1080p',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_file360p',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_file720p',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_fileThumbnail',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]