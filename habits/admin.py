

from django.contrib import admin
from .models import Exercise, Routine, Profile, DailyLog, Tip


admin.site.register(Exercise)
admin.site.register(Routine)
admin.site.register(Profile)
admin.site.register(DailyLog)
admin.site.register(Tip) 