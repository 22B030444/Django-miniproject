# Generated by Django 5.1.3 on 2024-11-19 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], max_length=10),
        ),
    ]
