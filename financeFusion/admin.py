from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Transaction)
admin.site.register(models.Budget)
admin.site.register(models.Goal)
admin.site.register(models.Category)
