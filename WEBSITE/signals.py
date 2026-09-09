from pathlib import Path

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Episode, Genre, Movie


FILE_FIELDS = {
    Movie: ("poster_image", "backdrop_image", "video_file", "download_file", "trailer_file"),
    Episode: ("thumbnail_image", "video_file", "download_file"),
}


def delete_file(field_file):
    if field_file and field_file.name:
        try:
            field_file.delete(save=False)
        except (FileNotFoundError, OSError):
            pass


def old_file(instance, field_name):
    if not instance.pk:
        return None
    try:
        old = type(instance).objects.get(pk=instance.pk)
    except type(instance).DoesNotExist:
        return None
    field = getattr(old, field_name, None)
    return field.name if field else None


@receiver(pre_save, sender=Movie)
@receiver(pre_save, sender=Episode)
def remove_replaced_files(sender, instance, **kwargs):
    for field_name in FILE_FIELDS[sender]:
        old_name = old_file(instance, field_name)
        new_field = getattr(instance, field_name, None)
        new_name = new_field.name if new_field else None
        if old_name and old_name != new_name:
            try:
                getattr(sender.objects.get(pk=instance.pk), field_name).delete(save=False)
            except (sender.DoesNotExist, FileNotFoundError, OSError):
                pass


@receiver(post_delete, sender=Movie)
@receiver(post_delete, sender=Episode)
def remove_deleted_files(sender, instance, **kwargs):
    for field_name in FILE_FIELDS[sender]:
        delete_file(getattr(instance, field_name, None))
