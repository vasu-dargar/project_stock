from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db import models
from .models import Symbol, User, UserSymbol
from django.http import HttpResponse
from django.template import loader
import requests
import json
import sys

#SIGNUP MODULE
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            count=User.objects.all().count()

            #USER CREATION
            u=User(user_id=count+1,user_name=username)
            u.save()

            User.objects.all().order_by('user_id')
            messages=["Signup successful"]
            return render(request, 'profile.html', {'messages': messages})
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
#SIGNIN MODULE  
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

#WISHLIST INFORMATION MODULE  
def profile(request):
    if request.user.is_authenticated:
        user=User.objects.get(user_id=request.user.id)

        #RETRIEVING SYMBOLS OF SIGNED-IN USER
        usersymbols=UserSymbol.objects.filter(user=user)
        symbols = []
        for obj in usersymbols:
            symbols.append(obj.User_symbol)
        count = len(symbols)

        #DISPLAY INFORMATION OF STOCK SYMBOLS IN WISHLIST OF SIGNED-IN USER
        info={}
        for symbol in symbols:
            url = "https://www.alphavantage.co/query"
            data_params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol.name,
                "interval":"5min",
                "outputsize": "compact",
                "apikey": "1WBN904SDOEK21FJ",
                }
            j=requests.get(url, params=data_params)
            data=j.json()
            latest_time=data["Meta Data"]["3. Last Refreshed"]
            info[symbol.name]={"Last Refreshed":data["Meta Data"]["3. Last Refreshed"],"Interval":data["Meta Data"]["4. Interval"],"Time Zone":data["Meta Data"]["6. Time Zone"],"Latest stock value":data["Time Series (5min)"][latest_time]["4. close"]}
        template = loader.get_template('profile.html')
        context = {
            'symbols': symbols,
            'info': info,
            'count': count,
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('profile.html')
        context = {}
        return HttpResponse(template.render(context, request))

#MODULE FOR DISPLAYING STOCK SYMBOLS IN WISHLIST OF SIGNED-IN USER
def display(request): 
    user=User.objects.get(user_id=request.user.id)
    usersymbols=UserSymbol.objects.filter(user=user)
    symbols = []
    for obj in usersymbols:
        symbols.append(obj.User_symbol)
    template = loader.get_template('add-remove.html')
    context = {
        'symbols': symbols,
    }
    return HttpResponse(template.render(context, request))

#SIGNOUT MODULE
def signout(request):
    logout(request)
    return redirect('/')

#MODULE TO ADD STOCK SYMBOLS IN WISHLIST OF SIGNED-IN USER
def add(request):
    if request.method == 'POST':
        name=request.POST.get('sname')
        user=User.objects.get(user_id=request.user.id)
        symbol=Symbol.objects.filter(name=name)
        
        #ADDING STOCK SYMBOL TO SIGNED-IN USER
        if symbol.count()==0:
            count=Symbol.objects.all().count()
            symbol=Symbol(sid=count+1,name=name)
            symbol.save()
            Symbol.objects.all().order_by('sid')
            count1=UserSymbol.objects.all().count()
            usersymbol=UserSymbol(u_s_id=count1+1,user=user,User_symbol=symbol)
            usersymbol.save()
            UserSymbol.objects.all().order_by('u_s_id')
        else:
            for s in symbol:
                count1=UserSymbol.objects.all().count()
                usersymbol=UserSymbol(u_s_id=count1+1,user=user,User_symbol=s)
                usersymbol.save()
                UserSymbol.objects.all().order_by('u_s_id')

    template = loader.get_template('add.html')
    context = {}
    return HttpResponse(template.render(context, request))

#DELETING STOCK SYMBOLS FROM WISHLIST OF SIGNED-IN USER
def remove(request,name):
    user=User.objects.get(user_id=request.user.id)
    symbols=Symbol.objects.filter(name=name)
    x=0
    for symbol in symbols:
        usersymbols=UserSymbol.objects.filter(user=user,User_symbol=symbol)
        for user_symbol in usersymbols:
            x=user_symbol.u_s_id
            count=UserSymbol.objects.all().count()
            #DELETE SELECTED STOCK SYMBOL OF SIGNED-IN USER
            user_symbol.delete()

            UserSymbol.objects.all().order_by('u_s_id')

            #RE-ASSIGNING IDs OF EVERY UserSymbol OBJECTS NEXT IN TABLE AFTER THE DELETED ONE
            for y in range(x+1,count+1):
                temp_usersymbol=UserSymbol.objects.get(u_s_id=y)
                temp_symbol_name=temp_usersymbol.User_symbol.name
                temp_user=temp_usersymbol.user
                temp_usersymbol.delete()
                UserSymbol.objects.all().order_by('u_s_id')
                temp_symbols=Symbol.objects.filter(name=temp_symbol_name)
                if temp_symbols.count()==0:
                    count_symbols=Symbol.objects.all().count()
                    new_symbol=Symbol(sid=count_symbols + 1,name=temp_symbol_name)
                    new_symbol.save()
                    Symbol.objects.all().order_by('sid')
                    new_usersymbol=UserSymbol(u_s_id=y-1,user=temp_user,User_symbol=new_symbol)
                    new_usersymbol.save()
                    UserSymbol.objects.all().order_by('u_s_id')
                else:
                    for temp_symbol in temp_symbols:
                        new_usersymbol=UserSymbol(u_s_id=y-1,user=temp_user,User_symbol=temp_symbol)
                        new_usersymbol.save()  
                        UserSymbol.objects.all().order_by('u_s_id') 

    usersymbols=UserSymbol.objects.filter(user_id=request.user.id).order_by('u_s_id')
    symbols_list=[]
    for usersymbol in usersymbols:
        symbols_list.append(usersymbol.User_symbol)
    template = loader.get_template('add-remove.html')
    context = {
        'symbols': symbols_list,
    }
    return HttpResponse(template.render(context, request))