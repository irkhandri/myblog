from .models import Author, Interest
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchingAuthor (request):

    some_query = ''

    if request.GET.get("some_query"):
        some_query = request.GET.get("some_query")
    
    interests = Interest.objects.filter(name__iexact = some_query)

    authors = Author.objects.distinct().filter(
        Q(name__icontains = some_query) |
        Q(email__icontains = some_query) |
        Q(username__icontains = some_query) |
        Q(location__icontains = some_query) |
        Q(intro__icontains = some_query) |
        Q(bio__icontains = some_query) |
        Q(interest__in = interests)
    )

    return some_query, authors




def paginateAuthors (request, res, authors):
    page = request.GET.get('page')
    paginator = Paginator(authors, res)

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        authors = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        authors = paginator.page(page)

    first_page = (int(page) - 3)
    if first_page < 1:
        first_page = 1
    
    last_page = (int(page) + 3)
    if last_page > paginator.num_pages:
        last_page = paginator.num_pages + 1
    

    my_range = range(first_page, last_page)

    return my_range, authors
