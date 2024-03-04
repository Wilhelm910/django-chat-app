from django.shortcuts import render, redirect
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.core import serializers

# def create_user_view(request):
#     #if request.method == "POST" and request.POST.get("username", "") and request.POST.get("email", "") and request.POST.get("password", ""):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password1"]
#             user = authenticate(username=username, password=password)
#             login(request,user)
#             return redirect("/chat/")
#         # user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"))
#         # user.save()
#         # if user:
#         #     return HttpResponseRedirect("/login/")
#     else:
#         form = UserCreationForm()
#     return render(request, "create_user/create_user.html", {"form": form})


def create_user_view(request):
    if request.method == "POST" and request.POST.get("username", "") and request.POST.get("email", "") and request.POST.get("password", ""):
         if request.method == "POST":
            user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"))
            user.save()
            if user:
                return HttpResponseRedirect("/chat/")
    return render(request, "create_user/create_user.html", )


def login_view(request):
    redirect=request.GET.get("next")
    if request.method == "POST" and request.POST.get("username", "") and request.POST.get("password", ""):
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request,user)
           # return HttpResponseRedirect("/chat/")
            return HttpResponseRedirect(request.POST.get("redirect"))
        else:
            return render(request, "auth/login.html", {"wrongPassword": True, "redirect": redirect}, )
    return render(request, "auth/login.html", {"redirect": redirect})


@login_required(login_url="/login/")
def index(request):
    if request.method == "POST" and request.POST.get("textmessage", ""):
        print("received data " + request.POST["textmessage"])
        newChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST["textmessage"], chat=newChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [ new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    else:
        print("Input field empty or not POST method")
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {"messages": chatMessages, "current_user": request.user})


def logout_view(request):
    logout(request)
    return redirect("/login/?next=/chat/")

