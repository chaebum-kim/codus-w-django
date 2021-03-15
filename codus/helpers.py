from django.utils import timezone
from uuid import uuid4


def make_path_and_rename(instance, filename):
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    ymd_path = timezone.now().strftime('%y/%m/%d')
    uuid_name = uuid4().hex
    extension = filename.split('.')[-1].lower()
    return '/'.join([
        app_label,
        cls_name,
        ymd_path,
        uuid_name + '.' + extension,
    ])
