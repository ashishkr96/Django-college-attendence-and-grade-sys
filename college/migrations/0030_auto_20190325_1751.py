# Generated by Django 2.1.4 on 2019-03-25 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0029_auto_20190325_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.Semester'),
        ),
    ]
