from django.contrib import admin
from .models import create_project, Review
# Register your models here.
admin.site.register(create_project)
admin.site.register(Review)