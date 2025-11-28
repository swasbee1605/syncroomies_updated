from django.db import models

class Message(models.Model):
    sender = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
