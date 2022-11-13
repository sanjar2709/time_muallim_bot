from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True, default="-----")
    tg_id = models.BigIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name_plural = "Users"


class Post(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False, related_name="post_users")
    file_id = models.CharField(max_length=300, null=False, blank=False)
    caption = models.CharField(max_length=1000, null=True, blank=True)
    post_type = models.SmallIntegerField(choices=[(1, "image"), (2, "video"), (3, "audio"), (4, "text")], default=2,
                                         null=False, blank=False)
    channel = models.CharField(max_length=100, null=True, blank=True)
    send_time = models.DateTimeField(null=True, blank=True)

    send_post = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.user}" or f"{self.file_id}" or "---"

    class Meta:
        verbose_name_plural = "Post"
        ordering = ["-created_at"]


class Log(models.Model):
    tg_id = models.BigIntegerField(null=False, blank=False, unique=True)
    message = models.JSONField(null=False, blank=False, default={})

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "#%s" % self.tg_id

    class Meta:
        verbose_name_plural = "Foydalanuvchilar Loglari"
        ordering = ['-created_at']