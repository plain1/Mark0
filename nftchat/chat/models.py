from django.db import models
from django.conf import settings
from mint.models import Register

class Room(models.Model):
    Token_id = models.TextField()
    Token_uri = models.TextField()
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # 유저모델과 연결한다.
        blank=True,
        related_name = 'rooms')  # 룸이라는 인덱스 지정.
    
    def __str__(self):
        return self.room_name
         
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    room = models.ForeignKey(Room, related_name='messages', default=1, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content



