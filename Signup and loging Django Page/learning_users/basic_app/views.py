from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


#for authenticate and check for login and logout
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("you are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered=False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            #saving password in database in encrypted form
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            #one to one relation for users
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

                profile.save()

                registered= True

        else :
            print(user_form.errors,UserProfileInfoForm.errors)

    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render (request,'basic_app/registration.html',{'user_form':user_form,
                                                          'profile_form':profile_form,
                                                          'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account is not active !")

        else:
            print("Unknown login")
            print("username :{} and password {} ".format(username,password))
            return HttpResponse("invalid login details !")
    else:
        return render(request,'basic_app/login.html',{})
