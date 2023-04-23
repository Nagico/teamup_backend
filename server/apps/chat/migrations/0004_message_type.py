# Generated by Django 4.2 on 2023-04-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_remove_message_type_alter_message_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="type",
            field=models.IntegerField(
                choices=[(0, "未知"), (1, "聊天消息"), (2, "确认")],
                default=0,
                verbose_name="消息类型",
            ),
        ),
    ]