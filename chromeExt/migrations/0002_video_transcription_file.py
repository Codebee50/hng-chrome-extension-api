# Generated by Django 4.2 on 2023-09-29 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chromeExt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='transcription_file',
            field=models.FileField(null=True, upload_to='transcriptions/'),
        ),
    ]