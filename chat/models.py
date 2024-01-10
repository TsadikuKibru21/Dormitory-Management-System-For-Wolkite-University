from django.db import models

from account.models import UserAccount

class Messages(models.Model):

    description = models.TextField()
    sender_name = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='senders')
    receiver_name = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='receivers')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)

class Friends(models.Model):

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"
