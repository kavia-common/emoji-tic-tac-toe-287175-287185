from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "next_player", "winner", "is_draw", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
