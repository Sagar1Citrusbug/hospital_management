# Generated by Django 4.2.6 on 2023-11-03 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("appointment", "0001_initial"),
        ("doctor", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="doctor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
            ),
        ),
    ]
