# importing api
from django.shortcuts import render, redirect
from newsapi import NewsApiClient
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth, messages

# Create your views here.


def index(request):

    newsapi = NewsApiClient(api_key='957c8067be9244c192ddf9dfac14542a')
    top = newsapi.get_top_headlines(sources='techcrunch')

    l = top['articles']
    desc = []
    news = []
    img = []

    for i in range(len(l)):
        f = l[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
    mylist = zip(news, desc, img)

    return render(request, 'index.html', context={"mylist": mylist})


def about(request):
    return render(request, 'about.html')


# def login(request):
#     return render(request, 'login.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in!")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken!")
            return redirect("register")
        else:
            user = User.objects.create_user(
                name=name,
                username=username,
                password=password,
                email=email,
            )
            auth.login(request, user)
            messages.success(request, "You are logged in!")
            return redirect("/")
    else:
        return render(request, "register.html")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are logged out!")
        return redirect("/")

    #     form = NewUserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         messages.success(request, "Registration successful.")
    #         return redirect("/")
    #     messages.error(
    #         request, "Unsuccessful registration. Invalid information.")
    # form = NewUserForm()
    # return render(request=request, template_name="register.html", context={"register_form": form})
