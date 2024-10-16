from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Create_task(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    title=models.CharField(max_length=255)
    description=models.TextField()
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Not Started')

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    is_completed=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)

    clear_datetime = models.TimeField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return self.title
    

class Assign_task(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]

    title=models.CharField(max_length=255)
    description=models.TextField()
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Not Started')
    assigned_by=models.ForeignKey(User,on_delete=models.CASCADE, related_name='tasks_assigned_by',null=True)
    assign_to=models.ForeignKey(User,on_delete=models.CASCADE, related_name='tasks_assigned_to')
    deadline=models.DateField()

    is_completed=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.title
