from django.contrib import admin

from app import models

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)

# Register your models here.
