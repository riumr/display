from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()


class Index(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_article = models.ForeignKey(Article, on_delete=models.CASCADE)
