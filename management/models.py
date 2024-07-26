from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Adds a 'role' field to differentiate between different user roles.

    """
    Roles=(
        ('admin','Admin'),
        ('manager','Manager'),
        ('member','Member')
    )
    role=models.CharField(max_length=10,choices=Roles,default='member')

class Project(models.Model):
    """
    Model representing a project.
    Each project has a name, description, creation date, and an owner.

    """
    name=models.CharField(max_length=100)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

class Task(models.Model):
    """
    Model representing a task within a project.
    Each task is associated with a project, and can be assigned to a user.

    """
    
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    assigned_to=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    due_date=models.DateTimeField()
    status=(
        ('completed','completed'),
        ('pending','pending')
    )
    status=models.CharField(max_length=10,choices=status,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class Milestone(models.Model):
    """
    Model representing a milestone within a project.
    Each milestone has a name, description, due date, and timestamps for creation and update.

    """
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    due_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Notification(models.Model):
    """
    Model representing a notification for a user.
    Each notification has a message, creation date, and a read status.
    
    """
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)



