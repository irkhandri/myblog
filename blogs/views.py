from django.shortcuts import render, redirect
from .models import Blog, Tag
from django.utils import timezone
from .util import countTime, searchingQuery, paginateBlogs
from .forms import BlogForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required(login_url='login')
def createBlog (request):

    form = BlogForm()
    author = request.user.author

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = author
            blog.save()

            for tag in newtags:
                tag, create = Tag.objects.get_or_create(
                    name=tag
                )
                blog.tags.add(tag) 

            messages.success(request, "Blog created!!")
            return redirect('account')
        
    context = {
        'form' : form,
        'todo' : 'Create',
        'object' : 'blog',
    }

    return render(request, 'blogs/blog_form.html', context)


@login_required(login_url='login')
def updateBlog (request, pk):
    author = request.user.author
    blog = author.blog_set.get(id=pk)
    form = BlogForm(instance=blog)

    if request.method=="POST":

        newtags = request.POST.get('newtags').replace(',', " ").split()

        form=BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            for tag in newtags:
                tag, create = Tag.objects.get_or_create(
                    name=tag
                )
                blog.tags.add(tag)
            return redirect('account')
    
    context = {'form' : form}
    return render(request, 'blogs/blog_form.html', context=context)


@login_required(login_url='login')
def deleteBlog (request, pk):
    blog = Blog.objects.get(id=pk)

    if request.user.author.id != blog.owner.id:
        return redirect('account')
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request,'Blog deleted!')
        return redirect('account')
    
    context = {
        'obj' : blog,
    }
    return render (request, 'delete_template.html', context)



def blogs(request):

    some_query, blogs = searchingQuery(request)

    # blogs = Blog.objects.all()

    res = 2

    my_range, blogs = paginateBlogs(request, res, blogs)



    context = {
        'blogs' : blogs,
        'some_query' : some_query,
        'paginator' : my_range,

    }

    return render (request, 'blogs/blogs.html', context)



def blog(request, pk):

    form = CommentForm()
    blogObj = Blog.objects.get(id=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.owner = request.user.author
        comment.blog = blogObj
        comment.save()
        blogObj.countReaction

        messages.success(request, "Your comment wass successfulllly addded!")
        return redirect('blog', pk=blogObj.id)


    time = countTime(blogObj.created)
    context = {
        'blog' : blogObj,
        'time' : time,
        'form' : form,
    }

    return render(request, 'blogs/blog.html' , context)


