# Generated by Django 4.2 on 2023-04-11 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("activities", "0001_initial"),
        ("teams", "0003_team_public"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="activity",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="activities.activity",
                verbose_name="所属赛事",
            ),
        ),
    ]
