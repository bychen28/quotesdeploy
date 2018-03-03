from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
	return redirect('/main')

def loginpage(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if 'id' not in errors:
            request.session['status'] = "register"
        for tag,error in errors.iteritems():
            messages.error(request,error,extra_tags = tag)
            return redirect('/main')
        else:
            request.session['id'] = errors['id']
            return redirect('/dashboard')
    return redirect('/main')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if 'id' not in errors:
            request.session['status'] = "login"
            for tag, error in errors.iteritems():
                messages.error(request,error, extra_tags = tag)
            return redirect('/main')
        else:
            request.session['id'] = errors['id']
            return redirect('/dashboard')
    return redirect('/main')

def logout(request):
    request.session.clear()
    return redirect('/main')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/main')
    else:
        user = User.objects.get(id = request.session['id'])
        wallquotes = user.posted_quote.all()
        myquotes = user.favorited_quotes.all()
        favlist = Quote.objects.all().exclude(favorite_quotes = request.session['id'])
        
        context = {
            'user': user,
            'thewallquotes': wallquotes,
            'myownquotes': myquotes,
            'myfavlist': favlist
        }
        return render(request, 'dashboard.html', context)

def makequote(request):
    if 'id' not in request.session:
        return redirect('/main')
    else:
        return redirect('/dashboard')

def addquote(request):
    if request.method =="POST":
        errors = Quote.objects.validate_quote(request.POST)
        if 'success' not in errors:
            for tag,error in errors.iteritems():
                messages.error(request,error,extra_tags = tag)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    return redirect('/main')


def showitem(request, iid):
    if 'id' not in request.session:
        return redirect('/main')
    else:
        user = User.objects.get(id = request.session['id'])
        quoteid = Quote.objects.get(id = iid)
        myposts = user.posted_quote.all()

    context = {
        'user': user,
        'item': quoteid,
        'posts': myposts
    }
    return render(request,'showitem.html', context)

def addfavquote(request, iid):
    if 'id' not in request.session:
        return redirect('/main')
    else:
        this_user = User.objects.get(id = request.session['id'])
        this_quote = Quote.objects.get(id = iid)
        this_quote.favorite_quotes.add(this_user)
        return redirect('/dashboard')

def remove(request, iid):
    if 'id' not in request.session:
        return redirect('/main')
    else:
        this_user = User.objects.get(id = request.session['id'])
        this_quote = Quote.objects.get(id = iid)
        this_quote.favorite_quotes.remove(this_user)
        return redirect('/dashboard')
    pass