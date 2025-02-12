# Generated by Django 5.0.6 on 2024-07-06 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "code",
                    models.CharField(max_length=3, primary_key=True, serialize=False),
                ),
                ("abbr", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("minimal", models.IntegerField(null=True)),
                ("maximum", models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Salary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("minimal", models.IntegerField(null=True)),
                ("maximum", models.IntegerField(null=True)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacancy.currency",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vacancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("employment", models.CharField(max_length=50)),
                ("schedule", models.CharField(max_length=20)),
                ("description", models.TextField()),
                ("href", models.CharField(max_length=255)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacancy.company",
                    ),
                ),
                (
                    "experience",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vacancy.experience",
                    ),
                ),
                (
                    "salary",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vacancy.salary",
                    ),
                ),
            ],
        ),
    ]
