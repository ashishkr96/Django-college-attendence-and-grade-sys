# Generated by Django 2.1.4 on 2019-03-25 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0028_auto_20190325_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sem',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='college.Semester'),
        ),
    ]