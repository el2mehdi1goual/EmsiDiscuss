"""
Administration pour l'application Votes
"""
from django.contrib import admin
from .models import TopicVote, ReplyVote

@admin.register(TopicVote)
class TopicVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__username', 'topic__id')
    readonly_fields = ('created_at',)

@admin.register(ReplyVote)
class ReplyVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'reply', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__username', 'reply__id')
    readonly_fields = ('created_at',)
