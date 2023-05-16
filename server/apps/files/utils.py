import datetime

from django.conf import settings
from files.models import File
from zq_django_util.utils.oss.utils import (
    get_random_name,
    get_token,
    split_file_name,
)


def gen_token(filename, request, user):
    name, ext = split_file_name(filename)
    file = File.objects.create(user=user, name=name, ext=ext)

    callback_dict = {
        "callbackUrl": f"{settings.SERVER_URL}/api/files/{file.id}/callback/",
        "callbackBody": "file=${object}&size=${size}",
        "callbackBodyType": "application/x-www-form-urlencoded",
    }

    token = get_token(
        key=f"media/files/{get_random_name(filename)}",
        callback=callback_dict,
    )

    res = {
        "file_id": file.id,
        **token,
    }

    return res


def handle_callback(instance: File, request):
    url = request.data.get("file")
    name = url.lstrip(settings.MEDIA_URL.lstrip("/"))

    instance.file.name = name
    instance.size = request.data.get("size")

    instance.update_time = datetime.datetime.now()
    instance.save()

    return instance
