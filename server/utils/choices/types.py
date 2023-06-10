from django.db import models


class FileType(models.IntegerChoices):
    """
    文件类型状态
    """

    UNKNOWN = 0, "未知"
    FEEDBACK = 1, "反馈"


class GenderType(models.IntegerChoices):
    """
    性别，主要用于用户表
    """

    UNKNOWN = 0, "未知"
    MALE = 1, "男"
    FEMALE = 2, "女"


class DegreeType(models.IntegerChoices):
    """
    学位
    """

    UNKNOWN = 0, "未知"
    BACHELOR = 1, "学士"
    MASTER = 2, "硕士"
    DOCTOR = 3, "博士"


class FeedbackType(models.IntegerChoices):
    """
    反馈类型
    """

    UNKNOWN = 0, "未知"
    ACTIVITY = 1, "赛事添加"
    USAGE = 2, "使用困难"
    INFORMATION = 3, "信息错误"
    BAN = 4, "封禁反馈"
    OTHER = 5, "其他"


class MessageType(models.IntegerChoices):
    """
    消息类型
    """

    UNKNOWN = 0, "未知"
    CHAT = 1, "聊天消息"
    READ = 2, "已读回执"
    IMAGE = 3, "图片消息"
    TEMPLATE = 4, "模板消息"
