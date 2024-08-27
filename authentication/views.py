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
from django.contrib.auth.password_validation import password_changed,UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from .custom_authentication import EmailorUsernameModelBackend
from .forms import MobileForm,EmailReset
from address.models import UserAddress,area,country_choice,city,state
from django.urls import reverse 
from .forms import UpdateMobileForm
from django.db.models import Q
from cart.models import Cart
from .tests import update_mobile_send_otp,create_mobile_send_otp
from datetime import datetime
import pyotp
import os 
import json
from django.http.response import JsonResponse
from address.views import state_and_lga
from dotenv import load_dotenv
load_dotenv()
#from .custom_authentication2 import EmailorUsernameModelBackend

# Create your views here.

#forget password view. User input username or email and we search if user exists in our data base.
def email_reset_password(request):
    #form = EmailReset()
    if request.method == "POST":
        try:
            username_or_mail = request.POST.get("email").strip()
            if username_or_mail:
            
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
            else:
                messages.error(request, "User details does not exist in our database! Be sure to input a correct email or username.")
                return redirect('authentication:email_reset_password')
        except:
            messages.error(request, "User details does not exist in our database! Be sure to input a correct email or username.")
            return redirect('authentication:email_reset_password')

    return render(request,'authentication/email_reset_kunkky.html',{})


def create_mobilenumber_otp(request):
    #This view is to create phone number for a user.
    if request.method == "POST":
        otp = request.POST.get("otp")
    
        otp_secret = request.session['otp_secret_key']  
        valid_date = request.session['otp_valid_date']
        if otp_secret and valid_date is not None:
            valid_date = datetime.fromisoformat(valid_date)
            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret, interval=60)
                if totp.verify(otp):
                    session_create_number = request.session['create_phone_number']
                    model = Mobile.objects.create(user=request.user,phone_no=session_create_number)
                    del session_create_number
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    messages.success(request, "You have successfully created PHONE NUMBER!")
                    return redirect('authentication:account_info')
                else:
                    messages.error(request, "Invalid one time password")
                    return redirect('authentication:otp')
            else:
                messages.error(request, "One time password has expired")
                return redirect('authentication:edit_account')
        else:
            messages.error(request, "Ooops! Something went wrong")
            return redirect('authentication:otp')

    return render(request,'authentication/create_mobilenumber_otp.html',{})


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
    
    try:
        if request.method == "POST":
            form = request.POST.get("mobile_no").strip()
            
            if len(form) == 0:
                messages.error(request, "PHONE NUMBER field must be filled")
                return redirect('authentication:mobile')
            if len(form) > 14 or len(form) < 14:
                messages.error(request, "PHONE NUMBER must be 11 digits!")
                return redirect('authentication:mobile')
            else: 
                request.session['create_phone_number'] = form
                messages.success(request, "Please, input the one time password sent to " + form)
                create_mobile_send_otp(request)
                return redirect('authentication:create_mobilenumber_otp')
    except AttributeError:
        pass
    except ConnectionError:
        messages.error(request, "Please, be sure to check your internet connection!\nIf you did not receive your otp, try again but ensure that your internet is on.")
        return redirect('authentication:mobile')   

    return render(request,'authentication/mobile.html',{})


def all(request):

    return render(request,'authentication/all_signups.html')


def signup(request):
    session_username = ""
    session_fname = ""
    session_lname = ""
    session_email = ""

    if request.method == "POST":
        username = request.POST.get("username").strip()
        fname = request.POST.get("fname").strip()
        lname = request.POST.get("lname").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        password2 = request.POST.get("password2").strip()
        
        try:
            request.session['username'] = username
            request.session['fname'] = fname
            request.session['lname'] = lname
            request.session['email'] = email
        except KeyError:
            pass

        username = username.lower()
        email = email.lower()
        password = password.lower()
        password2 = password.lower()

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
            try:
                session_user = User.objects.get(username=request.session['username'])
            except:
                pass 
            if session_user is not None:
                del request.session['username']
                del request.session['fname']
                del request.session['lname']
                del request.session['email']
            #Daniel, do not forget to set user.is_active = False during deployment.
            user.is_active = False
        
            #Welcome mail
            try:
                subject = 'Welcome mail from Adimeals.com'
                body = render_to_string('welcome_mail.html',{
                    'name':fname
                }) 
                from_email = EMAIL_HOST_USER
                to = [user.email]
                email = EmailMultiAlternatives(
                    subject,
                    body,
                    from_email,
                    to,
                )
                email.content_subtype = "html"
                fail_silently = True
                email.send()
            except:
                pass
    

            #Email Confirmation
            try: 
                current_site = get_current_site(request) 
                subject = 'Email confirmation from Adimeals.com'
                body = render_to_string('email_confirmation.html',{
                    'name':fname,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                }) 
                from_email = EMAIL_HOST_USER
                to = [user.email]
                email = EmailMultiAlternatives(
                    subject,
                    body,
                    from_email,
                    to,
                )
                email.content_subtype = "html"
                fail_silently = True
                email.send()

                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                return redirect('authentication:signin')
        
            except:
                messages.success(request,"Your account has been successfully created!\nWe have also sent you a confirmation email, please confirm your email address to login into your account.")
                return redirect('authentication:signin')
    else:
        pass
    try:
        session_username = request.session['username']  
        session_fname = request.session.get('fname')
        session_lname = request.session.get('lname') 
        session_email = request.session.get('email')
    except:
        pass
    
    return render(request,'authentication/signup_kunkky.html',{
        'username':session_username,
        'fname':session_fname,
        'lname':session_lname,
        'email':session_email,
    })


def signin(request):
    user_address = ""
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        remember_me = request.POST.get("checkbox")
        
        username = username.lower()
        password = password.lower()

        user = EmailorUsernameModelBackend.authenticate(EmailorUsernameModelBackend,request,username,password)
        #Daniel, do not forget to add "and user.is_active == False during deployment"
        if user is not None and user.is_active == False:
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
            try:
                user_address = UserAddress.objects.get(user=request.user)
            except UserAddress.DoesNotExist:
                pass
            if user_address is None:    
                messages.success(request, "You have successfully logged in")
                return redirect('address:register_address')
            else:
                messages.success(request, "You have successfully logged in")
                return redirect('home')

        else:
            messages.error(request, "Bad credentials! or Check your mail to verify account if you have not!")
            return redirect('authentication:signin')

    return render(request,'authentication/signin_kunkky.html')


def signout(request):

    logout(request)
    messages.success(request, "You have successfully signed out!")
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
    address = ""
    fname = ""
    lname = ""
    email = ""
    address = ""
    phone = ""
    try:
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
        address = UserAddress.objects.get(user=request.user)
        phone = Mobile.objects.get(user=request.user)
        
    except UserAddress.DoesNotExist:
        messages.info(request, "Please, kindly fill in your address")
        return redirect(reverse('address:register_address'))
    except AttributeError:
        pass
    except Mobile.DoesNotExist:
        messages.info(request, "Please, kindly fill in your phone number")
        return redirect(reverse('authentication:mobile'))
    except Exception as e:
        messages.info(request, "Oooops!! Something went wrong.")
        return redirect(reverse('address:register_address'))

    return render(request,'authentication/account_info.html',{'names':[uname,fname,lname,email,phone,address]})

def updatenumber_otp(request):
    #This view is to update phone number for a user.
    if request.method == "POST":
        otp = request.POST.get("otp")

        otp_secret = request.session['otp_secret_key']  
        valid_date = request.session['otp_valid_date']
        if otp_secret and valid_date is not None:
            valid_date = datetime.fromisoformat(valid_date)
            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret, interval=60)
                if totp.verify(otp):
                    model = Mobile.objects.get(user=request.user)
                    model.phone_no = request.session['update_mobile']
                    model.save()
                    del request.session['update_mobile']
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    messages.success(request, "You have successfully updated your PHONE NUMBER!")
                    return redirect('authentication:account_info')
                else:
                    messages.error(request, "Invalid one time password")
                    return redirect('authentication:otp')
            else:
                messages.error(request, "One time password has expired")
                return redirect('authentication:edit_account')
        else:
            messages.error(request, "Ooops! Something went wrong")
            return redirect('authentication:otp')

    return render(request,'authentication/otp.html',{})



def edit_account(request):
    #This is a view to edit a user's account information

    #What I did here is, I first of all listed out all the details of the user currently logged in 
    #Then I got all the user inputs from the "Edit info template"
    #After which I got the User object, then inserted each new input from edit info template.

    #Here I added a Phone number form to this view to update phone number
    
    form = ""
    try:
        model = Mobile.objects.get(user=request.user)

        if request.method == "POST":
            form = request.POST.get("update_mobile_no").strip()
            if len(form) == 0:
                messages.info(request, "PHONE NUMBER unchanged!")
                return redirect('authentication:account_info')
            elif len(form) > 14 or len(form) < 14:
                messages.error(request, "PHONE NUMBER must be 14 digits!")
                return redirect('authentication:edit_account')
            elif form == model.phone_no:
                messages.error(request, "Phone number already in use by you. Change number to proceed")
                return redirect('authentication:edit_account')
            else:
                request.session['update_mobile'] = form
                print(form)
                messages.success(request, "Please, input the one time password sent to " + form)
                update_mobile_send_otp(request)
                return redirect('authentication:otp')    
    
    except AttributeError:
        pass
    except Mobile.DoesNotExist:
        messages.info(request, "Please, complete account information before editing account")
        return redirect('address:register_address')
    except ConnectionError:
        messages.error(request, "Please, be sure to check your internet connection!\nIf you did not receive your otp, redirect back to the previous page, and ensure your internet is on.")
        return redirect('authentication:account_info')
    

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
        
            uname = uname.lower()
            email = email.lower()

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
    
    
    
    try:
        user = UserAddress.objects.get(user=request.user)
        if request.method == "POST":
            state = request.POST.get("state")
            division = request.POST.get("division")
            lga = request.POST.get("lga")
            lcda = request.POST.get("lcda")
            street_name = request.POST.get("street_name")
            
            user.state = state
            user.division = division
            user.lga = lga
            user.lcda = lcda
            user.street_name = street_name
            user.save()
            messages.success(request, "You have successfully updated address.")
            return redirect('authentication:account_info')
    except:
        pass
        
    return render(request,'authentication/edit_account.html',{'state_lga':state_and_lga.items()})



def change_address(request):#division
    if request.method == "POST":
        data = json.loads(request.body)
        address_value = data.get('division_id')
        divisions = state_and_lga.get(address_value, {})
        response_data = list(divisions.keys())
        return JsonResponse(response_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def change_address_division(request):#lga
    if request.method == "POST":
        data = json.loads(request.body)
        division_value = data.get('lga_id')
        selected_state = data.get('state')
        divisions_selsect = state_and_lga.get(selected_state, {})
        lga = divisions_selsect.get(division_value).keys()
        return JsonResponse(list(lga), safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def change_address_lga(request):#lcda
    if request.method == "POST":
        data = json.loads(request.body)
        lcda = data.get('lcda_id')
        selected_state = data.get('state')
        selected_division = data.get('division')
        lga = data.get('lga')
        state = state_and_lga.get(selected_state, {})
        lcda_list = state.get(selected_division).get(lga)

        return JsonResponse(lcda_list, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


#This is a page to reset password while user is logged in 
def setpassword(request):
    try:
        username = request.user.username
        if request.method == "POST":
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()
            
            password = password.lower()
            password2 = password2.lower()

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

            password = password.lower()
            password2 = password2.lower()
    
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
