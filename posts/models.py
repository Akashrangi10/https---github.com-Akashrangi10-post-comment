
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class AllUsers(AbstractUser):
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    name = models.ForeignKey(AllUsers,on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to ="posts",blank=True,null=True)
    post_desc = models.TextField(max_length=1000,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Like(models.Model):
    user = models.ForeignKey(AllUsers, on_delete=models.CASCADE, related_name="users")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts")
    like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.post}"



class Comments(models.Model):
    name = models.ForeignKey(AllUsers,on_delete=models.CASCADE,default = True,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    droped_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}-{self.body}"

class MyProfileDetails(models.Model):
    username = models.ForeignKey(AllUsers,models.CASCADE)
    profile_pic = models.ImageField(upload_to ="ProfilePhotos",blank=True,null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    bio = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.username}"