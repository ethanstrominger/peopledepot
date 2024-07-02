# Generated by Django 4.2.11 on 2024-07-01 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_event_could_attend_event_must_attend_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPermissions",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "permission_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.permissiontype",
                    ),
                ),
                (
                    "practice_area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.practicearea",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.project"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="userpermissions",
            constraint=models.UniqueConstraint(
                fields=("user", "permission_type", "project", "practice_area"),
                name="unique_user_permission",
            ),
        ),
    ]
