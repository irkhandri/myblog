from django.db import models
from users.models import Author
# Create your models here.


class Blog(models.Model):

    owner = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    image = models.ImageField(null=True, blank=True, default='default.png')

    tags = models.ManyToManyField('Tag', blank=True)

    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_like = models.IntegerField(default=0, null=True, blank=True)
    vote_dislike = models.IntegerField(default=0, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(unique=True, primary_key=True)

    @property
    def commentators (self):
        res = self.comment_set.all().values_list('owner__id', flat=True)
        return res

    
    def __str__(self):
        return self.title 
    
    @property
    def countReaction(self):
        reactions = self.comment_set.all()
    
        self.vote_like = reactions.filter(react='like').count()
        self.vote_dislike = reactions.filter(react='dislike').count()
        self.vote_total = reactions.count()
        
        self.save()

    class Meta:
        ordering = ['-vote_like']


class Tag(models.Model):

    name = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(unique=True, primary_key=True)

    def __str__(self):
        return self.name
    


class Comment (models.Model):

    vote_set = (
            ("like", "Like"),
            ("dislike", "Dislike")
    )
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    blog =  models.ForeignKey(Blog, on_delete=models.CASCADE)

    react = models.CharField(max_length=200, choices=vote_set)
    description = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(primary_key=True, unique=True)

    class Meta:
        unique_together = [['owner', 'blog']]
    

    def __str__(self):
        return self.react
    
