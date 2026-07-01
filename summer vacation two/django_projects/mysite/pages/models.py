from django.db import models
from django.contrib.auth.models import User
# Create your models here

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)
    passed = models.BooleanField(null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.user.username}-{self.level}-{self.submitted_at}"