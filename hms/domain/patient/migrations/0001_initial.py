# Generated by Django 4.2.6 on 2023-10-09 10:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
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
                ("name", models.CharField(max_length=60)),
                ("dob", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("MALE", "Male"),
                            ("FEMALE", "Female"),
                            ("OTHER", "Other"),
                        ],
                        max_length=6,
                    ),
                ),
                ("contact_no", models.CharField(max_length=15)),
                ("address", models.CharField(max_length=250)),
            ],
            options={
                "db_table": "patient",
            },
        ),
    ]