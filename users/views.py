from django.shortcuts import render, redirect
from .forms import CreatorUserForm, InterestForm, AuthorForm, MessageForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .models import Author, Interest, Message
from blogs.models import Blog
from .utils import searchingAuthor, paginateAuthors



# Create your views here.

def users (request):

    some_query, authors = searchingAuthor(request)
    # authors = Author.objects.all()
    my_range, authors = paginateAuthors(request, 3, authors)

    context = {
        'authors' : authors,
        "some_query" : some_query,
        'paginator' : my_range,

    }
    return render (request, 'users/users.html', context)

def user (request, pk):

    author = Author.objects.get(id=pk)

    if pk == request.user.id:
        return redirect('account')

    if author == request.user:
        return redirect('account')


    interests = author.interest_set.all()
    context = {
        "author" : author,
        "interests" : interests,
    }

    return render(request, 'users/user.html', context)


@login_required(login_url='login')
def authorEdit (request, pk):

    author = Author.objects.get(id=pk)
    form = AuthorForm(instance=author)

    if request.method == 'POST':
        form = AuthorForm(request.POST,request.FILES, instance=author)
        author = form.save()
        messages.success(request,'Information edited!')
        return redirect('account')



    context = {
        'form' : form,
        'todo' : "Update",
        'object' : 'profile',
    }

    return render(request, 'form_template.html', context)


@login_required(login_url='login')
def interestCreate (request):

    author = request.user.author
    form = InterestForm()

    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.owner = author
            interest.save()
            messages.success(request,'Interest was added!')
            return redirect('account')

    context = {
        'form' : form,
        'todo' : "Create",
        'object' : 'interest',
    }
    return render (request, 'form_template.html', context)



@login_required(login_url='login')
def interestEdit (request, pk):

    interest = Interest.objects.get(id=pk)
    form = InterestForm(instance=interest)

    if request.method == "POST":
            form = InterestForm(request.POST, instance=interest)
            form.save()
            messages.success(request,'Interest edited!')

            return redirect('account')


    context = {
        'form' : form,
        'todo' : "Update",
        'object' : 'interest',
    }
    return render (request, 'form_template.html', context)


@login_required(login_url='login')
def interestDelete (request, pk):
    interest = Interest.objects.get(id=pk)

    if request.method == "POST":
        interest.delete()
        messages.success(request,'Interest deleted!')
        return redirect('account')

    context = {
        'obj' : interest,
    }
    return render (request, 'delete_template.html', context)




def registerUser (request):
    page = 'register'
    form = CreatorUserForm()

    if request.method == 'POST':
        form = CreatorUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account create!')


            login(request, user)

            author = Author.objects.create(
                user = user,
                name = user.first_name,
                email = user.email,
                username = user.username
            )

            return redirect('users')
        else :
            messages.error(request, 'An error has occurred during registration!')
    
    context = {'form' : form,         'page' : page}
    return render(request, 'users/login_signup.html', context)


def loginUser (request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('account')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = None
        try:
            user = Author.objects.get(username=username)
        except:
            messages.error(request, 'Wrong username')
        
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect ( request.GET['next'] if 'next' in request.GET else 'account')
        else: 
            messages.error(request, "Wrong input")
        

    context = {
        'page' : page
    }

    return render (request, 'users/login_signup.html', context)


def logoutUser (request) :

    logout(request)
    messages.success(request, 'Logout Succes')


    return redirect('register')


def account (request):

    account = Author.objects.get(id=request.user.id)
      
    interests = account.interest_set.all()

    blogs = account.blog_set.all()


    # for i in blogs:
    #     time.append(countTime(i.created))

        #info = [account.intro, account.location, account.email,account.mobil]
    context = {
        'account' : account,
        'interests' : interests,
        'blogs' : blogs,
        
        #'info' : info,
    }
    return render (request, 'users/account.html', context)


# @login_required(login_url='login')
# def boxMessages(request):





@login_required(login_url='login')
def inputMessages(request):

    box = 'intbox'

    author = request.user.author
    objectsMess = author.messages.all()
    unread = objectsMess.filter(is_read=False).count()

    context = {
        'objMessages' : objectsMess,
        'unread' : unread,
        'box' : box,

    }
    return render (request, 'users/input_messages.html', context)


@login_required(login_url='login')
def outputMessages(request):

    box = 'outbox'
    author = request.user.author
    objectsMess = author.out_messages.all()
    # unread = objectsMess.filter(is_read=False).count()

    context = {
        'objMessages' : objectsMess,
        'box' : box,
        # 'unread' : unread,
    }
    return render (request, 'users/output_messages.html', context)


@login_required(login_url='login')
def currentMessage(request, pk):

    author = request.user.author
    # objMessage = author.messages.get(id=pk)
    objMessage = Message.objects.get(id=pk)

    if objMessage.is_read == False and author == objMessage.recipient:
        objMessage.is_read = True
        objMessage.save()
        # if 'next' in request.GET :
        #     return redirect(request.GET['next'])
    


    context = {
        'mess' : objMessage,
    }
    return render (request, 'users/message.html', context)


def createMessage (request, pk):

    recipient = Author.objects.get(id=pk)

    form = MessageForm()

    try:
        sender = request.user.author
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            
            if sender:
                message.name = sender.name
                message.email = sender.email

            message.sender = sender
            message.recipient = recipient

            message.save()
            messages.success(request, "Your message was!")

            return redirect('user', pk=recipient.id)

    context = {
        'form' : form,
        'recipient' : recipient,
    }
    return render (request, 'users/message_template.html', context)
