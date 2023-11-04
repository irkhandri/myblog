from django.contrib import admin
from .models import Author, Interest, Message

# Register your models here.

admin.site.register (Author)
admin.site.register (Interest)
admin.site.register (Message)
