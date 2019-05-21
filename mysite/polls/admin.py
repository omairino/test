from django.contrib import admin
from .models import User,FacebookLabel,FacebookPage

admin.site.register(User)
admin.site.register(FacebookPage)
admin.site.register(FacebookLabel)