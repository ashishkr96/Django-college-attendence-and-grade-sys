# Generated by Django 2.1.4 on 2019-03-25 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0024_auto_20190325_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='college.Student'),
        ),
    ]