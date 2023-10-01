# Generated by Django 4.2 on 2023-10-01 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chromeExt', '0003_remove_video_transcription_file_video_transcript'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField()),
                ('chunks', models.BinaryField(null=True)),
            ],
        ),
    ]