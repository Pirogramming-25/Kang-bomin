from django.db import models

# Create your models here.

class Review(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.CharField(max_length=200)
    score = models.IntegerField()
    director = models.CharField(max_length=200)
    actor = models.CharField(max_length=200)
    running_time = models.IntegerField()
    content = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
