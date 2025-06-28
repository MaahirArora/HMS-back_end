# from django.db.models.signals import post_save, pre_save, post_delete
# from django.dispatch import receiver
# from .models import Student, Room

# @receiver(pre_save, sender=Student)
# def update_room_occupied_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         # New student, will handle in post_save
#         return

#     # Get previous room before update
#     try:
#         old_student = Student.objects.get(pk=instance.pk)
#         old_room = old_student.room
#     except Student.DoesNotExist:
#         old_room = None

#     new_room = instance.room

#     if old_room != new_room:
#         if old_room:
#             old_room.occupied = max(0, old_room.occupied - 1)
#             old_room.save()
#         if new_room:
#             new_room.occupied += 1
#             new_room.save()

# @receiver(post_save, sender=Student)
# def increment_occupied_on_create(sender, instance, created, **kwargs):
#     if created:
#         if instance.room:
#             room = instance.room
#             room.occupied += 1
#             room.save()

# @receiver(post_delete, sender=Student)
# def decrement_occupied_on_delete(sender, instance, **kwargs):
#     if instance.room:
#         room = instance.room
#         room.occupied = max(0, room.occupied - 1)
#         room.save()
from django.apps import AppConfig

class HostelConfig(AppConfig):
    name = 'hostel'
    verbose_name = 'Hostel Management'

    def ready(self):
        # this will import and register your signal handlers
        import hostel.signals  