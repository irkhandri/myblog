from django.utils import timezone
from .models import Blog, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def countTime(created):

    time_diff = timezone.now() - created 
    seconds = time_diff.seconds

    time = []
    time.append(time_diff.days)
    hours, remainder = divmod(seconds, 3600)
    time.append(hours)

    minutes, seconds = divmod(remainder, 60)

    time.append(minutes)
    time.append(seconds)

    return time



def searchingQuery (request):
    
    some_query = ''

    if request.GET.get('some_query'):
        some_query = request.GET.get('some_query')
    
    tags = Tag.objects.filter(name__icontains =  some_query)


    blogs = Blog.objects.distinct().filter(
        Q(title__icontains = some_query) |
        Q(description__icontains = some_query) |
        Q(tags__in = tags) |
        Q(owner__name__icontains = some_query)
    )


    return some_query, blogs


def paginateBlogs (request, res, blogs):
    page = request.GET.get('page')
    paginator = Paginator(blogs, res)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        blogs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        blogs = paginator.page(page)

    first_page = (int(page) - 3)
    if first_page < 1:
        first_page = 1
    
    last_page = (int(page) + 3)
    if last_page > paginator.num_pages:
        last_page = paginator.num_pages + 1
    

    my_range = range(first_page, last_page)

    return my_range, blogs


