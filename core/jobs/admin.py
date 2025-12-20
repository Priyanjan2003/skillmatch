from django.contrib import admin
from .models import Skill, Job

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('required_skills',)