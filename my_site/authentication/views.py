from audioop import reverse
from django.core.mail import EmailMessage,send_mail
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from my_site import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from .models import User 

# Create your views here.


def all(request):

    return render(request,'authentication/all_signups.html')


def signup(request):

    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")


        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "E-mail already exist!")
            return redirect('home')

        if len(username) > 15:
            messages.error(request, "Length of username too long!")
            return redirect('home')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')

        if not password.isalnum():
            messages.error(request, "Password must be alphanumeric!")
            return redirect('home')
          
        
        user = User.objects.create_user(username=username,email=email,password=password)
        user.fname = fname 
        user.is_active = False
        user.save()
        


        # Welcome E-mail

        subject = 'Welcome to ADi meals mobile!'
        message = f'Hello {fname.capitalize()}, welcome to ADi meals mobile!\n\nThank you for visiting our website.\n\nWe have also sent you a confirmation email, please confirm your email address to login into your account.\n\n\n\nThanking you.\n\n\nVictoria Oluwaseyi\nC.E.O'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)


        #Email Confirmation 
        current_site = get_current_site(request) 
        email_subject = 'Confirm your email @ ADi meals mobile!'
        message2 = render_to_string('email_confirmation.html',{
            'name':fname,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        }) 
        from_email2 = settings.EMAIL_HOST_USER
        to_list2 = [user.email]

        #email = EmailMessage(
            #email_subject,
            #message2,
            #settings.EMAIL_HOST_USER,
            #[user.email],
        #)
        #fail_silently = True
        #email.send()

        send_mail(email_subject,message2,from_email2,to_list2,fail_silently=True)


        messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
        
        return redirect('authentication:signin')

         
    return render(request,'authentication/signup.html')


def signin(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)


        if user is not None and user.is_active == False:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            fname = username
            return render(request,'authentication/landing_page.html',{'fname':fname})

        else:
            messages.error(request,"Bad credentials! or Check your mail to verify account!")
            return redirect('authentication:signin')


    return render(request,'authentication/signin.html')


def signout(request):

    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,user.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True 
        fname = user.fname 
        user.save()
        login(request, user)
        messages.success(request, "Email has been verified successfully!")
        return render(request,'authentication/landing_page.html',{'fname':fname})

    else:
        return render(request, 'activation_failed.html')


def account_info(request):

    return render(request,'authentication/account_info.html',{'names':[request.user.username,request.user.first_name,request.user.last_name,request.user.email]})


def edit_account(request):

    return render(request,'authentication/edit_account.html')


def setpassword(request):

    return render(request,'authentication/setpassword.html')





