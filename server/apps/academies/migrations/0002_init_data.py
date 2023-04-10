import json
from pathlib import Path

from django.db import migrations

JSON_PATH = Path(__file__).parent / "data" / "zq_academy.json"


def init_data(apps, schema_editor):
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    Academy = apps.get_model("academies", "Academy")
    Academy.objects.bulk_create(
        Academy(
            id=item["id"],
            level=item["level"],
            name=item["name"],
            parent_id=item["pid_id"],
        )
        for item in data
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("academies", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=init_data,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
