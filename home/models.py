from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class feedback(models.Model):
    email=models.CharField(max_length=20)
    name=models.CharField(max_length=15)
    phone=models.CharField(max_length=10)
    text=models.TextField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Medical(models.Model):
    sno=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    nameM=models.CharField(max_length=20)
    doses=models.TextField(max_length=10)
    frequency=models.TextField(max_length=10)
    
    def __str__(self):
        return self.user.username 
    

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username