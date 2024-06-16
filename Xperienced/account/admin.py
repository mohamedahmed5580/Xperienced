from django.contrib import admin
from .models import User
from .models import Skill
admin.site.register(Skill)
# Register your models here.
admin.site.register(User)
