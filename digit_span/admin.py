from django.contrib import admin
from .models import Test

@admin.register(Test)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'round', 'music', 'bothEars', 'score')
    ordering = ('id',)