
from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Routine(models.Model):
    LEVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    exercises = models.ManyToManyField(Exercise) 

    def __str__(self):
        return f"{self.name} ({self.level})"


class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed_routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    

class Profile(models.Model):
    LEVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Tip(models.Model):
    CATEGORY_CHOICES = [
        ('alimentacion', 'Alimentación'),
        ('sueño', 'Sueño'),
    ]
    content = models.TextField(help_text="El texto del consejo")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.get_category_display()} Tip - {self.content[:40]}...'