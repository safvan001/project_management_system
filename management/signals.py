# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Milestone,Notification
from .tasks import send_notification_email



@receiver(post_save, sender=Task)
def create_task_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.assigned_to, message=f'New task assigned: {instance.name}')

@receiver(post_save, sender=Milestone)
def create_milestone_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.project.owner, message=f'New milestone created: {instance.name}')

# @receiver(post_save, sender=Task)
# def task_post_save(sender, instance, created, **kwargs):
#     if created:
#         send_notification_email.delay(
#             instance.assigned_to.email,
#             f'New task "{instance.name}" has been assigned to you.'
#         )
#     else:
#         send_notification_email.delay(
#             instance.assigned_to.email,
#             f'Task "{instance.name}" has been updated.'
#         )

# @receiver(post_save, sender=Milestone)
# def milestone_post_save(sender, instance, created, **kwargs):
#     if created:
#         send_notification_email.delay(
#             instance.project.manager.email,
#             f'New milestone "{instance.name}" has been created for project "{instance.project.name}".'
#         )
#     else:
#         send_notification_email.delay(
#             instance.project.manager.email,
#             f'Milestone "{instance.name}" for project "{instance.project.name}" has been updated.'
#         )
