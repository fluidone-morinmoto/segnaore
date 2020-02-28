from django.contrib import admin
from .models import *
from . import logger

# Register your models here.
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(WorkedHours)

logger.info("Nel admin")
