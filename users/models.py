from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name     = models.CharField(max_length=200, null=True, blank=True)
    email    = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    intro    = models.CharField(max_length=200, null=True, blank=True)
    mobil    = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='authors/', default='authors/person.jpeg')

    soc_facebook = models.CharField(max_length=200, null=True, blank=True)
    soc_x        = models.CharField(max_length=200, null=True, blank=True)
    soc_youtube  = models.CharField(max_length=200, null=True, blank=True)
    soc_linkedin = models.CharField(max_length=200, null=True, blank=True)
    soc_telegram = models.CharField(max_length=200, null=True, blank=True)


    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(primary_key=True, unique=True)

    def __str__(self):
        return str(self.username)



class Interest (models.Model):

    owner = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(primary_key=True, unique=True)


    def __str__(self):
        return str(self.name)

class Message (models.Model):

    sender = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True,related_name="out_messages")
    recipient = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True,related_name="messages")

    subject = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField()
    email = models.EmailField(max_length=200, null=True, blank=True)

    name = models.CharField(max_length=200, null=True, blank=True)

    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(primary_key=True, unique=True)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read']