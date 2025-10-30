from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Task, Activity

# Store original status to compare on update
@receiver(pre_save, sender=Task)
def capture_old_status(sender, instance, **kwargs):
    if instance.pk:
        previous = Task.objects.get(pk=instance.pk)
        instance._previous_status = previous.status

@receiver(post_save, sender=Task)
def log_task_activity(sender, instance, created, **kwargs):
    user = instance.creator  # default to creator (adjust as needed)

    if created:
        Activity.objects.create(
            user=user,
            message=f"created task '{instance.title}' in project '{instance.project.name}'"
        )
    else:
        if hasattr(instance, "_previous_status") and instance.status == "completed" and instance._previous_status != "completed":
            Activity.objects.create(
                user=user,
                message=f"completed task '{instance.title}' in project '{instance.project.name}'"
            )
