from django.db import models

# Create your models here.

import uuid

from django_ckeditor_5.fields import CKEditor5Field

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4,)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True) #auto_now_add=True which means that the field is set to the current date and time when the object is first created, and it will not change on subsequent updates. auto_now=True means that the field is updated to the current date and time every time the object is saved.

    updated_at = models.DateTimeField(auto_now_add=True) #auto_now_add=True which means that the field is set to the current date and time when the object is first created, and it will not change on subsequent updates. auto_now=True means that the field is updated to the current date and time every time the object is saved.

    class Meta:

        abstract = True

class Project(BaseClass):

    name = models.CharField(max_length=255)

    description = CKEditor5Field()

    document = models.FileField(upload_to = 'project-documents')

    class Meta:

        verbose_name = 'Projects'

        verbose_name_plural = 'Projects'

    def __str__(self):

        return self.name


class AssignedProjects(BaseClass):

    project = models.ForeignKey('Project',on_delete=models.PROTECT,related_name='project')

    coordinator = models.ForeignKey('authentication.Profile',on_delete=models.PROTECT,related_name='coordinator')

    developers = models.ManyToManyField('authentication.Profile')

    project_duration = models.IntegerField()

    project_start_date = models.DateField()

    project_tentative_end_date = models.DateField()

    completed = models.BooleanField(default=False)

    completed_date =  models.DateTimeField(null=True,blank=True)

    class Meta:

        verbose_name = 'Assigned Projects'

        verbose_name_plural = 'Assigned Projects'

    def __str__(self):

        return f'{self.project.name} - {self.project_start_date}'

class PriorityChoices(models.TextChoices):
    Low = 'Low', 'Low'

    Medium = 'Medium', 'Medium'

    High = 'High', 'High'

class Task(BaseClass):

    assigned_project =  models.ForeignKey('AssignedProjects',on_delete=models.PROTECT,related_name='task_project')

    assigned_to = models.ForeignKey('authentication.Profile',on_delete=models.PROTECT,related_name='task_assigned_to')

    title = models.CharField(max_length=255)

    description = models.TextField()

    priority = models.CharField(max_length=15,choices=PriorityChoices.choices)

    duration = models.TimeField(null=True,blank=True)

    start_date = models.DateField(null=True,blank=True)

    end_date = models.DateField(null=True,blank=True)

    completed = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Tasks'

        verbose_name_plural = 'Tasks'

    def __str__(self):

        return f'{self.assigned_project.project.name}-{self.assigned_to.first_name}-{self.title}'




