from django.contrib import admin
from .models import Post, Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ["pk", "tg_id", "first_name"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "post_type", "channel", "send_time", "send_post", "is_active",
                    "created_at"]
    search_fields = ["created_at__date", "user__tg_id"]


admin.site.register(Post, PostAdmin)
admin.site.register(Users, UsersAdmin)
