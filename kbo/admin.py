from django.contrib import admin
from .models import Hitter, Pitcher, Team

@admin.register(Hitter)
class HitterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hitter._meta.get_fields() if field.name != "team"]

@admin.register(Pitcher)
class PitcherAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pitcher._meta.get_fields() if field.name != "team"]

@admin.register(Team)
class TeakAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']