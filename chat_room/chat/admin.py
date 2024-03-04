from django.contrib import admin
from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    fields = ("chat","text", "created_at", "author", "receiver")
    list_display = ("text", "created_at", "author", "receiver")
    search_fields = ("text",)

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
