# Generated by Django 4.2.6 on 2023-10-10 05:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "updated_by",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("appointment_date", models.DateField()),
                ("purpose", models.CharField(max_length=300)),
            ],
            options={
                "db_table": "appointment",
            },
        ),
    ]
