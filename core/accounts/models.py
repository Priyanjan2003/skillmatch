from django.db import models
from django.contrib.auth.models import User

MATCHING_CHOICES = [
    ('skills', 'Skill Based'),
    ('resume', 'Resume (ATS) Based'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField('jobs.Skill', blank=True)
    experience = models.PositiveIntegerField(default=0)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )
    matching_mode = models.CharField(
        max_length=10,
        choices=MATCHING_CHOICES,
        default='skills')
    def __str__(self):
        return self.user.username
