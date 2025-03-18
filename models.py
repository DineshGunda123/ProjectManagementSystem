from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
class create_team_member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False)
    email = models.EmailField(null=False)
    address = models.TextField(default='Hyderabad')
    contact=models.IntegerField(null=False,default='123456789')
    image = models.ImageField(upload_to='media/',null=True)
    gender=models.CharField(max_length=10,default="Male")
    categories = models.CharField(max_length=20)
    designations = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} ({self.id})'
class create_project(models.Model):
    projectname = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    project_manager = models.ForeignKey(create_team_member, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    team_members = models.ManyToManyField(create_team_member, related_name='projects')
    categories = models.CharField(max_length=50)
    categories = models.CharField(max_length=50)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.projectname      
    
class Task(models.Model):
    task = models.CharField(max_length=255)
    project = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    comments = models.TextField()

    def __str__(self):
        return self.task    
    
class Review(models.Model):
    project = models.ForeignKey(create_project, related_name='reviews', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    suggesionsonpreviouspreviousreview=models.TextField(blank=True,null=True)
    algorithmandblockdiagram=models.TextField(blank=True,null=True)
    datasets=models.TextField(blank=True,null=True)
    resultanlysis=models.TextField(blank=True,null=True)
    statusofpaper=models.TextField(blank=True,null=True)
    feedback = models.TextField(blank=True, null=True)
    class Meta:
        unique_together = ('project', 'order')

    def __str__(self):
        return f"Review {self.order} for {self.project.projectname}"    