from django.db import models

class DevTool(models.Model):
    name = models.CharField(max_length = 100)
    kind = models.CharField(max_length = 100)
    content = models.TextField()

    def __str__(self):
        return self.name

    
class Idea(models.Model):
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'idea/')
    content = models.TextField()
    interest = models.IntegerField(default = 0)

    devtool = models.ForeignKey(
        DevTool,
        on_delete = models.CASCADE,
        related_name = 'ideas',
    )

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
class IdeaStar(models.Model):
    idea = models.ForeignKey(
        Idea,
        on_delete = models.CASCADE,
        related_name = 'stars'
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('idea', 'user')