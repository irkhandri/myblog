from django.contrib.auth.models import User
from .models import Author

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        
        user = instance
        subject = "Welcome to MyBlog"
        message = "Hello HI Dobry den!"

        send_mail (
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


post_save.connect(createProfile,sender=User)  
post_save.connect(createProfile,sender=Author)  

