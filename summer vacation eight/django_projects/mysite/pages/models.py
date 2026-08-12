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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
class ShopItem(models.Model):
    CATEGORY_CHOICES = [
        ("general", "一般"),
        ("avatar", "角色"),
        ("background", "背景"),
        ("badge", "徽章"),
        ("powerup", "道具"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="general")
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=200,blank=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} - {self.price} points"
class UserItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem,on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=("user","item")
    def __str__(self):
        return f"{self.user.username} 擁有 {self.item.name}"

    
class Post(models.Model):
    level_id = models.CharField(max_length=100)  # e.g. chapter-1-level-1-1
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} - {self.level_id}"

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        
class LevelUnlock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "level")

    def __str__(self):
        return f"{self.user.username} 解鎖 {self.level}"
