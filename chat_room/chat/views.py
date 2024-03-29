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


def create_user_view(request):
    """
    View function for handling user registration.

    If the request method is POST and the required 'username', 'email', and 'password' fields are provided,
    creates a new user using the User model and redirects to the "/chat/" URL upon successful registration.

    If the request method is not POST or the required fields are not provided, renders the 'create_user.html' template
    to display the user registration form.
    """
    if request.method == "POST" and request.POST.get("username", "") and request.POST.get("email", "") and request.POST.get("password", ""):
         if request.method == "POST":
            user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"))
            user.save()
            if user:
                return HttpResponseRedirect("/chat/")
    return render(request, "create_user/create_user.html", )


def login_view(request):
    """
    View function for handling user login.

    Retrieves the 'next' parameter from the GET request, indicating the intended redirect after successful login.

    If the request method is POST and both 'username' and 'password' are provided in the POST data,
    attempts to authenticate the user using the provided credentials.

    If authentication is successful, logs in the user and redirects to the specified 'next' parameter or the default.
    If authentication fails, renders the login page with an indication of a wrong password.

    If the request method is not POST, or 'username' and 'password' are not provided, renders the login page
    with the 'redirect' parameter to handle login form display.
    """
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
def index(request, chat_id=None):
    """
    View function for rendering the chat index page.

    If the request method is POST and there is a non-empty 'textmessage' field in the request POST data,
    it processes the incoming message, creates a new Message object, and returns a JSON response.
    If the request method is not POST or the 'textmessage' field is empty, it prints a message.

    It retrieves existing chat messages associated with Chat ID 1
    and renders the 'chat/index.html' template, passing the messages and the current user to the template.

    """
    chat = None
    chatMessages = None
    print(chat_id)
    if chat_id is None:
        if not Chat.objects.exists():
            return redirect("/create_chat/")
        chats = Chat.objects.all()[0]
        # REDIRECT TO "/chat/first chat id in my chats objects"
        return redirect(f"/chat/{chats.id}/")
    if chat_id is not None:
      
        chat = Chat.objects.get(id=chat_id)
    if request.method == "POST" and request.POST.get("textmessage", ""):
        print("received data " + request.POST["textmessage"])
        # chat_id = 1
        # try:
        #     existing_chat = Chat.objects.get(id=chat_id)
        # except Chat.DoesNotExist:
        #     existing_chat = Chat.objects.create(id=chat_id)
       # newChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST["textmessage"], chat=chat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [ new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    else:
        print("Input field empty or not POST method")
    chatMessages = Message.objects.filter(chat__id=chat_id)
    chats = Chat.objects.all()
    return render(request, "chat/index.html", {"messages": chatMessages, "current_user": request.user, 'chats': chats})


def chat_messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    chat_messages = Message.objects.filter(chat=chat)
    return render(request, 'chat/chat_messages.html', {'messages': chat_messages, 'current_user': request.user, 'chat': chat})


def create_chat(request):
    if request.method == "POST":
        chat_title = request.POST.get("chat_title", "")
        new_chat = Chat.objects.create(title=chat_title)
        return redirect(f"/chat/{new_chat.id}/")
    chats = Chat.objects.all()
    return render(request, "create_chat/create_chat.html", {'chats': chats})
      

def logout_view(request):
    """
    View function for handling user logout.

    Logs out the currently authenticated user using Django's 'logout' function.

    Redirects the user to the login page ("/login/") with the 'next' parameter set to "/chat/"
    to ensure the user is redirected to the chat page after a successful login.

    """
    logout(request)
    return redirect("/login/?next=/chat/")


