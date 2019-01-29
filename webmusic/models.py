from django.db import models


# Create your models here.

class collect(models.Model):
    """
    收藏夹
    """
    user_name = models.CharField(max_length=30)
    song_id = models.CharField(max_length=10)
    corver_pic = models.CharField(max_length=500)
    song_src = models.CharField(max_length=500)
    song_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    song_user_name = models.CharField(max_length=100)
    ctime = models.DateTimeField(auto_now_add=True)
