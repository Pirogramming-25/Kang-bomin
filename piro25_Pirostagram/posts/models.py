from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    content = models.TextField(blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Story(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)


class StoryImage(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='stories/')