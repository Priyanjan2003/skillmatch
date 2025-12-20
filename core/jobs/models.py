from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.ManyToManyField(Skill)
    min_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    apply_link = models.URLField(blank=True)
    min_experience = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
