# Generated by Django 5.1.1 on 2024-10-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(max_length=100),
        ),
    ]
