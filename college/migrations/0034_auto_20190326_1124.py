# Generated by Django 2.1.4 on 2019-03-26 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0033_batchsubject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchsubject',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='batchsubject',
            name='subject',
        ),
        migrations.DeleteModel(
            name='BatchSubject',
        ),
    ]
