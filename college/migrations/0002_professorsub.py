# Generated by Django 2.1.4 on 2019-03-05 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.Professor')),
                ('subject', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='college.SemesterSub')),
            ],
        ),
    ]
