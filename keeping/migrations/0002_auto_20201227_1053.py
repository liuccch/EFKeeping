# Generated by Django 3.1.4 on 2020-12-27 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keeping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keeping.user'),
        ),
        migrations.AlterField(
            model_name='mylog',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keeping.user'),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keeping.user'),
        ),
    ]
