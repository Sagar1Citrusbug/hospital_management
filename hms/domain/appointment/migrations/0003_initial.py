# Generated by Django 4.2.6 on 2023-11-03 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("patient", "0001_initial"),
        ("appointment", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="patient.patient"
            ),
        ),
    ]
