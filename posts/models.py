from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE)  # el usuario que postea
    created = models.DateTimeField(auto_now_add=True)

# --------------------------------------------------------------------
# la clase meta es para ordenar segun cuando fueron creados los post
    class Meta:
        ordering = ['-created']

# -------------------------------------------------------------------
# para evitar que alguien vote mas de una vez


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
