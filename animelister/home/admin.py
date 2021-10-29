# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import UserRating, Anime, Seiyuu, Studio


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified", "rating", "anime", "user")
    list_filter = ("created", "modified", "anime", "user")


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "status",
        "aired",
        "source",
        "duration",
        "season",
    )
    list_filter = ("created", "modified", "genre")
    raw_id_fields = ("seiyuu", "users")
    search_fields = ("name",)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified", "name")
    list_filter = ("created", "modified")
    search_fields = ("name",)


@admin.register(Seiyuu)
class SeiyuuAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified", "name")
    list_filter = ("created", "modified")
    search_fields = ("name",)
