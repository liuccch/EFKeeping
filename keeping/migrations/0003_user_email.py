# Generated by Django 3.1.4 on 2020-12-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeping', '0002_auto_20201227_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]