from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from my_site.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string,get_template
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from .models import User 
from django.contrib.auth.password_validation import password_changed,validate_password,UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from .custom_authentication import EmailorUsernameModelBackend
from food_app.views import slug_view,slug_view2
#from .custom_authentication2 import EmailorUsernameModelBackend


# Create your views here.

def main(request):
    fname = ""
    try:
        fname = request.user.first_name
    except AttributeError:
        return redirect('authentication:signin')
    
    return render(request,'authentication/landing_page.html',{'fname':fname,'all':slug_view(),'all':slug_view2()})


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
            return redirect('authentication:signup')
        
        elif User.objects.filter(email=email):
            messages.error(request, "E-mail already exist!")
            return redirect('authentication:signup')
            
        elif len(username) > 15:
            messages.error(request, "Length of username too long!")
            return redirect('authentication:signup')

        elif password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('authentication:signup')


        elif password:
            try:
                UserAttributeSimilarityValidator().validate(password)
            except:
                messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                CommonPasswordValidator().validate(password)
            except:     
                messages.error(request,"Password too common and easy.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                MinimumLengthValidator().validate(password)
            except:
                messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                return redirect('authentication:signup')
            try:
                NumericPasswordValidator().validate(password)
            except:
                messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                return redirect('authentication:signup')

        
            user = User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
            #Daniel, do not forget to set user.is_active = False during deployment.
            user.is_active = True
        


            # Welcome E-mail
            try:
                subject = 'Welcome to ADi meals mobile!'
                message = f'Hello {fname.capitalize()}, welcome to ADi meals mobile!\n\nThank you for visiting our website.\n\nWe have also sent you a confirmation email, please confirm your email address to login into your account.\n\n\n\nThanking you.\n\n\nVictoria Oluwaseyi\nC.E.O'
                from_email = EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject,message,from_email,to_list,fail_silently=True)
            except:
                return render(request, 'authentication/connection_error.html')


            #Email Confirmation
            try: 
                current_site = get_current_site(request) 
                email_subject = 'Confirm your email @ ADi meals mobile!'
                message2 = render_to_string('email_confirmation.html',{
                    'name':fname,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }) 
                from_email2 = EMAIL_HOST_USER
                to_list2 = [user.email]
                email = EmailMultiAlternatives(
                    email_subject,
                    message2,
                    from_email2,
                    to_list2,
                )
                email.content_subtype = "html"
                fail_silently = True
                email.send()

                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
        
                return redirect('authentication:signin')
        
            except:
                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                return redirect('authentication:signin')

         
    return render(request,'authentication/signup.html')


def signin(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("checkbox")

        user = EmailorUsernameModelBackend.authenticate(EmailorUsernameModelBackend,request,username,password)
        #Daniel, do not forget to add "and user.is_active == False during deployment"
        if user is not None: #and user.is_active == False:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
                
            messages.success(request, "You have successfully logged in")
            fname = request.user.first_name
            return redirect('authentication:landing_page')

        else:
            messages.error(request, "Bad credentials! or Check your mail to verify account!")
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
    #This is a view that displays the current information of the user!
    #It displays the username, first name, last name and email. it also gives the user access to edit the account information.
    try:
        uname = ""
        fname = ""
        lname = ""
        email = ""
    
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
    except AttributeError:
        return redirect('authentication:signin')

    return render(request,'authentication/account_info.html',{'names':[uname,fname,lname,email]})


def edit_account(request):
    #This is a view to edit a user's account information

    #What I did here is, I first of all listed out all the details of the user currently logged in 
    #Then I got all the user inputs from the "Edit info template"
    #After which I got the User object, then inserted each new input from edit info template.
    
    try:
        user_uname = request.user.username
        user_fname = request.user.first_name
        user_lname = request.user.last_name
        user_email = request.user.email
    

    
        user = User.objects.get(username=user_uname)
    
        if request.method == "POST":
            uname = request.POST.get("username")       
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")

            if User.objects.filter(username=uname):
                messages.error(request, "Username has been taken!\nPlease, try another username.")
                return redirect('authentication:edit_account')
            elif User.objects.filter(email=email):
                messages.error(request, "Email has been taken!\nPlease, try another Email.")
                return redirect('authentication:edit_account')

            if uname == "":
                uname = user_uname
            else:
                user.username = uname
                user.save()
            if fname == "":
                fname = user_fname 
            else:
                user.first_name = fname 
                user.save()
            if lname == "":
                lname = user_lname
            else:
                user.last_name = lname
                user.save()
            if email == "":
                email = user_email
            else:
                user.email = email
                user.save()
            
            messages.success(request, "You have successfully updated your account details!")
            return redirect('authentication:account_info')
    except AttributeError:
        return redirect('authentication:signin')
        
        
    return render(request,'authentication/edit_account.html')



def setpassword(request):
    try:
        username = request.user.username
        if request.method == "POST":
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            user = User.objects.get(username=username)
    
            if password:
            
                if password != password2:
                    messages.error(request,"Passwords do not match!")
                    return redirect('authentication:setpassword')
                
                try:
                    UserAttributeSimilarityValidator().validate(password)
                except:
                    messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    CommonPasswordValidator().validate(password)
                except:
                    messages.error(request,"Password too common and easy.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    MinimumLengthValidator().validate(password)
                except:
                    messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    NumericPasswordValidator().validate(password)
                except:
                    messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                    return redirect('authentication:setpassword')
                try:
                    password_changed(password,user=User,password_validators=NumericPasswordValidator)
                except:
                    messages.error(request, "Old password cannot be used!\nPlease, try a new password.")
                    return redirect('authentication:setpassword')


                user.set_password(password)
                user.save()
                messages.success(request, "You have successfully changed your password!")
                return redirect('authentication:signin')
    except AttributeError:
        return redirect('authentication:signin')
        
    return render(request,'authentication/setpassword.html')



