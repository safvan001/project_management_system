# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Milestone,Notification
from .tasks import send_notification_email



@receiver(post_save, sender=Task)
def create_task_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a Task is created.

    Parameters:
    - sender: The model class that triggered the signal (Task).
    - instance: The actual instance of the Task model that was saved.
    - created: A boolean indicating whether a new instance was created (True) or an existing instance was updated (False).
    - **kwargs: Additional keyword arguments passed by the signal.

    When a Task is created, this function creates a Notification for the user to whom the task is assigned.
    """
    if created:
        Notification.objects.create(user=instance.assigned_to, message=f'New task assigned: {instance.name}')

@receiver(post_save, sender=Milestone)
def create_milestone_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a Milestone is created.

    Parameters:
    - sender: The model class that triggered the signal (Milestone).
    - instance: The actual instance of the Milestone model that was saved.
    - created: A boolean indicating whether a new instance was created (True) or an existing instance was updated (False).
    - **kwargs: Additional keyword arguments passed by the signal.

    When a Milestone is created, this function creates a Notification for the owner of the project to which the milestone belongs.
    """
    if created:
        Notification.objects.create(user=instance.project.owner, message=f'New milestone created: {instance.name}')

