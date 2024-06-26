from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from my_site.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from .models import User,Mobile 
from django.contrib.auth.password_validation import password_changed,validate_password,UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from .custom_authentication import EmailorUsernameModelBackend
from .forms import MobileForm,EmailReset
from address.models import UserAddress,area,country_choice,city,state
from django.urls import reverse 
from .forms import UpdateMobileForm
from django.db.models import Q
from django.http import HttpResponse
from cart.models import Cart

#from .custom_authentication2 import EmailorUsernameModelBackend


# Create your views here.

#forget password view. User input username or email and we search if user exists in our data base.
def email_reset_password(request):
    #form = EmailReset()
    if request.method == "POST":
        #form = EmailReset(request.POST)
        #form = request.POST.get("email")
        #if form.is_valid():
        username_or_mail = request.POST.get("email").strip()
        try:
            model = User.objects.get(Q(username=username_or_mail) | Q(email=username_or_mail))

            #Email Password reset
            try: 
                current_site = get_current_site(request) 
                email_subject = 'Password reset @ADimeals'
                message2 = render_to_string('email_password_reset.html',{
                    'name':model.first_name,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(model.pk)),
                    'token': generate_token.make_token(model)
                }) 
                from_email2 = EMAIL_HOST_USER
                to_list2 = [model.email]
                email2 = EmailMessage(
                    email_subject,
                    message2,
                    from_email2,
                    to_list2,
                )
                email2.content_subtype = "html"
                fail_silently = False
                email2.send()
                messages.success(request, "We have sent RESET PASSWORD link to your registered email address to reset your password!")
                return redirect('authentication:email_reset_password')
            except:
                messages.success(request, "We have sent RESET PASSWORD link to your registered email address to reset your password!")
                return redirect('authentication:email_reset_password')
        except:
            messages.error(request, "User details does not exist in our database! Be sure to input a correct email or username.")
            return redirect('authentication:email_reset_password')

    return render(request,'authentication/email_reset_kunkky.html',{})



def mobile(request):
    #I first created a form to get phone number input from user, then render the number as per the currrent user request in the account info template.
    try:
        mobile = Mobile.objects.get(user=request.user)
        if mobile is not None:
            return redirect('authentication:account_info')
        else:
            pass
          
    except:
        pass

    if request.method == "POST":
        mobile_form = request.POST.get("phone_no")
        mobile = Mobile.objects.create(user=request.user,phone_no=mobile_form)
        messages.success(request, "You have successfully added a mobile number!")
        return redirect('authentication:account_info')

    return render(request,'authentication/mobile.html',{})


def all(request):

    return render(request,'authentication/all_signups.html')


def signup(request):

    if request.method == "POST":
        username = request.POST.get("username").strip()
        fname = request.POST.get("fname").strip()
        lname = request.POST.get("lname").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        password2 = request.POST.get("password2").strip()


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
            user2 = User.objects.get(username=username)
            #Daniel, do not forget to set user.is_active = False during deployment.
            user.is_active = True
        
            #Welcome mail
            try:
                email_subject = 'Welcome mail @ADimealsmobile!'
                message = render_to_string('welcome_mail.html',{
                    'name':fname
                }) 
                from_email = EMAIL_HOST_USER
                to_list = [user2.email]
                email = EmailMultiAlternatives(
                    email_subject,
                    message,
                    from_email,
                    to_list,
                )
                email.content_subtype = "html"
                fail_silently = True
                email.send()
            except:
                pass
                #return render(request, 'authentication/connection_error.html',{'fname':fname})

            # Welcome E-mail
            #try:
            #    subject = 'Welcome to ADi meals mobile!'
            #    message = f'Hello {fname.capitalize()}, welcome to ADi meals mobile!\n\nThank you for visiting our website.\n\nWe have also sent you a confirmation email, please confirm your email address to login into your account.\n\n\n\nThanking you.\n\n\nVictoria Oluwaseyi\nC.E.O'
            #    from_email = EMAIL_HOST_USER
            #    to_list = [user2.email]
            #    send_mail(subject,message,from_email,to_list,fail_silently=False)
            #except:
            #    return render(request, 'authentication/connection_error.html',{'fname':fname})
                

            #Email Confirmation
            try: 
                current_site = get_current_site(request) 
                email_subject = 'Email confirmation @ADimealsmobile!'
                message2 = render_to_string('email_confirmation.html',{
                    'name':fname,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user2.pk)),
                    'token': generate_token.make_token(user2)
                }) 
                from_email2 = EMAIL_HOST_USER
                to_list2 = [user2.email]
                email2 = EmailMultiAlternatives(
                    email_subject,
                    message2,
                    from_email2,
                    to_list2,
                )
                email2.content_subtype = "html"
                fail_silently = True
                email2.send()

                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                return redirect('authentication:signin')
        
            except:
                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                return redirect('authentication:signin')

    return render(request,'authentication/signup_kunkky.html')


def signin(request):
    
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        remember_me = request.POST.get("checkbox")

        user = EmailorUsernameModelBackend.authenticate(EmailorUsernameModelBackend,request,username,password)
        #Daniel, do not forget to add "and user.is_active == False during deployment"
        if user is not None: #and user.is_active == False:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            try:
                cart = Cart.objects.get(session_id=request.session['cart_users'],is_paid=False)
                if Cart.objects.filter(user=request.user,is_paid=False).exists():
                    cart.user = None
                    cart.save()
                else:
                    cart.user = request.user
                    cart.save()
            except:
                pass
                
            messages.success(request, "You have successfully logged in")
            return redirect('address:register_address')

        else:
            messages.error(request, "Bad credentials! or Check your mail to verify account if you have not!")
            return redirect('authentication:signin')


    return render(request,'authentication/signin_kunkky.html')


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
        return render(request,'home.html',{'fname':fname})
    else:
        return render(request, 'activation_failed.html')
    

def activate2(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,user.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        return redirect(reverse('authentication:reset',args=[uid,token]))

    else:
        return render(request, 'activation_failed.html')

        

def account_info(request):
    #This is a view that displays the current information of the user!
    #It displays the username, first name, last name and email. it also gives the user access to edit the account information.
    try:
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
        address = UserAddress.objects.get(user=request.user)
        phone = Mobile.objects.get(user=request.user)
        
    except:
        messages.error(request, "Please, kindly fill in your address first!")
        return redirect(reverse('address:register_address'))

    return render(request,'authentication/account_info.html',{'names':[uname,fname,lname,email,phone,address]})


def edit_account(request):
    #This is a view to edit a user's account information

    #What I did here is, I first of all listed out all the details of the user currently logged in 
    #Then I got all the user inputs from the "Edit info template"
    #After which I got the User object, then inserted each new input from edit info template.

    #Here I added a Phone number form to this view to update phone number
    
    model = Mobile.objects.get(user=request.user) 
    form = ""
    try:
        if request.method == "POST":
            form = request.POST.get("mobile_no").strip()
            
            if len(form) == 0:
                messages.info(request, "PHONE NUMBER unchanged!")
                return redirect('authentication:account_info')
            elif len(form) > 11 or len(form) < 11:
                messages.error(request, "PHONE NUMBER must be 11!")
                return redirect('authentication:edit_account')
            else:    
                model.phone_no = form
                model.save()
            messages.success(request, "You have successfully updated your PHONE NUMBER!")
            return redirect('authentication:account_info')
    except AttributeError:
        pass

    try:
        user_uname = request.user.username
        user_fname = request.user.first_name
        user_lname = request.user.last_name
        user_email = request.user.email
    
        user = User.objects.get(username=user_uname)
    
        if request.method == "POST":
            uname = request.POST.get("username").strip()       
            fname = request.POST.get("fname").strip()
            lname = request.POST.get("lname").strip()
            email = request.POST.get("email").strip()

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
        pass
    
    
    user = UserAddress.objects.get(user=request.user)
    try:
        if request.method == "POST":
            country_address = request.POST.get("country")
            state_address = request.POST.get("state")
            city_address = request.POST.get("city")
            area_address = request.POST.get("area")
            street_name_address = request.POST.get("street_name")
            
            user.country = country_address
            user.state = state_address
            user.city = city_address
            user.area = area_address
            user.street_name = street_name_address
            user.save()
            messages.success(request, "You have successfully updated address.")
            return redirect('authentication:account_info')
    except:
        pass
        
    return render(request,'authentication/edit_account.html',{'country':country_choice,'state':state,'city':city,'area':area,})


#This is a page to reset password while user is logged in 
def setpassword(request):
    try:
        username = request.user.username
        if request.method == "POST":
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()

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


#This is a view to reset password by e-mail or username when user forgets password 
def password_reset_by_mail(request, uid, token):
    try:
        user = User.objects.get(username=uid)
        if request.method == "POST":
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()
    
            if password:
            
                if password != password2:
                    messages.error(request,"Passwords do not match!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                
                try:
                    UserAttributeSimilarityValidator().validate(password)
                except:
                    messages.error(request,"Password too similar to user attribute provided.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                    CommonPasswordValidator().validate(password)
                except:
                    messages.error(request,"Password too common and easy.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                    MinimumLengthValidator().validate(password)
                except:
                    messages.error(request,"Only a minimum characters of 8 is allowed.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                    NumericPasswordValidator().validate(password)
                except:
                    messages.error(request,"Numeric only password is not allowed.\nPlease, try another password!")
                    return redirect(reverse('authentication:reset',args=[uid,token]))
                try:
                   password_changed(password,user=User,password_validators=NumericPasswordValidator)
                except:
                    messages.error(request, "Old password cannot be used!\nPlease, try a new password.")
                    return redirect(reverse('authentication:reset',args=[uid,token]))

                user.set_password(password)
                user.save()
                messages.success(request, "You have successfully changed your password!")
                return redirect(reverse('authentication:reset',args=[uid,token]))
    except AttributeError:
        return redirect('authentication/connection_error.html')
        
    return render(request,'authentication/reset.html')
