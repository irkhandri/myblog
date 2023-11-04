from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Interest, Message


class CreatorUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'username', 'email', 'password1', 'password2'
        ]

        labels = {
            'first_name' : 'Name'
        }




class InterestForm(ModelForm):

    class Meta:
        model = Interest
        fields = [
            'name', 'description'
        ]
        labels = {
            'name' : 'Title',
            'description' : 'Description',
        }
    

class AuthorForm (ModelForm):

    class Meta:
        model = Author
        fields = ['name', 'email', 'username', 'location', 'intro', 
                  'mobil', 'bio', 'image', 'soc_facebook', 'soc_x', 'soc_youtube', 
                    'soc_linkedin', 'soc_telegram']
        

class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['name','email', 'subject', 'text', ]

        labels = {
            'name' : 'Your name',
            'email' : 'Your email',
        }