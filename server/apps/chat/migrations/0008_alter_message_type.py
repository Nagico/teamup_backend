# Generated by Django 4.2 on 2023-05-16 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0007_alter_message_content_alter_message_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="type",
            field=models.IntegerField(
                choices=[(0, "未知"), (1, "聊天消息"), (2, "已读回执")],
                default=0,
                verbose_name="消息类型",
            ),
        ),
    ]